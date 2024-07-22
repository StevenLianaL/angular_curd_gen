import shutil
from dataclasses import dataclass
from pathlib import Path

import MySQLdb
from jinja2 import FileSystemLoader, Environment
from parse import parse
from pydantic import BaseModel
from MySQLdb.cursors import DictCursor
from angular_curd_gen.admin import ModelAdmin
from angular_curd_gen.config import TEMPLATE_DIR, BACKEND_TEMPLATE_DIR, FRONTEND_TEMPLATE_DIR
from angular_curd_gen.field import FieldUtil


@dataclass
class ModelRegister:
    model_admin: ModelAdmin = None
    model: BaseModel = None

    app_name: str = ''  # app name run in code
    app_readable_name: str = ''  # show in page
    app_title_name = ''

    db_name: str = 'test'
    db_user: str = 'test'
    db_pswd: str = 'test'

    db_list = []
    db_field_count = {}
    db_field_values = {}
    db_first_id = 0
    db_last_id = 0

    # extract model_pos info
    model_name = ''  # is single
    models_name = ''  # is plural
    lower_model_name = ''
    lower_models_name = ''
    model_fields_map = None  # all model_pos fields with type dict[str,type]
    jinja_env = None
    output_angular_dir = ''

    # extract model_pos admin info
    model_admin_fields = ()

    def register(self):
        """run all"""
        self._prepare()
        gen_functions = [i for i in dir(self) if i.startswith('gen_')]
        for f in gen_functions:
            getattr(self, f)()

        self._to_test_folder()

    def _prepare(self):
        # model_pos

        self.app_title_name = self.app_name.title()

        self.model_name = FieldUtil.to_singular(self.model.__name__)
        self.models_name = FieldUtil.to_plural(self.model_name)

        self.lower_model_name = FieldUtil.camel_to_snake(self.model_name)
        self.lower_models_name = FieldUtil.camel_to_snake(self.models_name)
        self.lower_model_camel_name = FieldUtil.snake_to_camel_lower(self.lower_model_name)

        self.model_fields_map = self.model.__dict__['__annotations__']

        # model_pos admin
        self.model_admin_fields = tuple([i for i in dir(self.model_admin) if not i.startswith('_')])
        if not self.model_admin.model_translate_fields:
            self.model_admin.model_translate_fields = self.model_admin.model_fields

        # template
        loader = FileSystemLoader(TEMPLATE_DIR)
        self.jinja_env = Environment(loader=loader)
        self.jinja_env.filters['to_camel'] = FieldUtil.snake_to_camel
        self.jinja_env.filters['to_lower_camel'] = FieldUtil.snake_to_camel_lower

        self.out_app_dir = Path(f"{self.app_name}")

        self.out_rust_dir = self.out_app_dir / BACKEND_TEMPLATE_DIR

        self.output_angular_dir = self.out_app_dir / FRONTEND_TEMPLATE_DIR / self.app_name
        self.output_angular_lower_model_name_dir = self.output_angular_dir / self.lower_model_name

        self._prepare_dirs()

        self._prepare_data()

    def _prepare_dirs(self):
        for attr in dir(self):
            if attr.endswith('_dir'):
                attr_value: Path = getattr(self, attr)
                if not attr_value.exists():
                    attr_value.mkdir(parents=True, exist_ok=True)

    def _prepare_data(self):
        """Query model_pos data, to count frontend component."""
        db_config = {
            'host': 'localhost',
            'user': self.db_user,
            'passwd': self.db_pswd,
            'db': self.db_name
        }
        db = MySQLdb.connect(**db_config, cursorclass=DictCursor)
        cursor = db.cursor()

        # data
        cursor.execute(f"select * from {self.lower_models_name};")
        self.db_list = cursor.fetchall()
        try:
            self.db_first_id = self.db_list[0]['id']
            self.db_last_id = self.db_list[-1]['id']
        except IndexError:
            self.db_first_id = 0
            self.db_last_id = 0

        # field count
        sql = ("select " +
               ",".join([f"COUNT(DISTINCT {f}) AS {f}" for f in self.model_admin.model_fields])
               + f" from {self.lower_models_name};")
        cursor.execute(sql)
        data = cursor.fetchone()
        self.db_field_count = data

        # field unique values
        for f in self.model_admin.model_fields:
            sql = f"select {f} from {self.lower_models_name};"
            cursor.execute(sql)
            values_data = cursor.fetchall()
            self.db_field_values[f] = set([d[f] for d in values_data])

    def _load_template(self, name: str):
        return self.jinja_env.get_template(name)

    def _draw_template(self, template_name: str, target: str, project: str = 'angular'):
        """
        :param template_name:
        :param target:
        :param project: angular/rust
        :return:
        """
        print(f"draw template {template_name=} to {target=} {project=}")
        template = self._load_template(template_name)
        context = self._build_context()
        rendered_content = template.render(context)
        match project:
            case 'angular':
                output_file = self.output_angular_dir / target
            case 'rust':
                output_file = self.out_rust_dir / target
            case _:
                raise ValueError(f"not support project {project}")

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open('w', encoding='utf8') as file:
            file.write(rendered_content)

    def _draw_component(self, component_name: str, level: str = 'model_pos'):
        templates = ['ts', 'css', 'html', 'spec.ts']
        for template in templates:
            template_name = f'{component_name}_component/{template}.jinja'
            match level:
                case 'model_pos':
                    target_prefix = f"{self.lower_model_name}-{component_name}"
                    father_dir = self.output_angular_dir / self.lower_model_name / target_prefix
                    target_dir = f"{self.lower_model_name}/{target_prefix}"
                case 'app':
                    target_prefix = f"{self.app_name}-{component_name}"
                    father_dir = self.output_angular_dir / target_prefix
                    target_dir = f"{target_prefix}"
                case _:
                    raise ValueError(f"not support level {level}")
            father_dir.mkdir(parents=True, exist_ok=True)
            target = f"{target_dir}/{target_prefix}.component.{template}"
            self._draw_template(template_name=template_name, target=target, project='angular')

    @staticmethod
    def extract_py_type(t):
        type_str = parse("<class '{type}'>", str(t))
        if not type_str:  # option
            type_str = parse("typing.Optional[{type}]", str(t))
        the_type = type_str.named['type']
        if '.' in the_type:
            the_type = the_type.split('.')[-1]
        return the_type

    def map_ts_type(self, t):
        the_type = self.extract_py_type(t)

        match the_type:
            case 'int' | 'float':
                return 'number'
            case 'str' | 'Image' | 'Url':
                return 'string'
            case 'bool':
                return 'boolean'
            case 'datetime' | 'date':
                return 'Date'
            case _:
                raise ValueError(f"not support type {t}")

    def map_ts_type_default(self, t):
        the_type = self.extract_py_type(t)
        match the_type:
            case 'int' | 'float':
                return '0'
            case 'str' | 'Image' | 'Url':
                return "''"
            case 'bool':
                return 'null'
            case 'datetime' | 'date':
                return 'null'
            case _:
                raise ValueError(f"not support type {t}")

    def map_rust_type(self, t):
        the_type = self.extract_py_type(t)

        match the_type:
            case 'int':
                return 'i64'
            case 'float':
                return 'f64'
            case 'str' | 'Image' | 'Url':
                return 'String'
            case 'bool':
                return 'bool'
            case 'datetime':
                return 'DateTime'
            case '  date':
                return 'NaiveDate'
            case _:
                raise ValueError(f"not support type {t}")

    def _build_context(self) -> dict:
        base_context = {
            'app_name': self.app_name,
            'app_readable_name': self.app_readable_name,
            'app_title_name': self.app_title_name,
            'model_name': self.model_name,
            'models_name': self.models_name,
            'lower_models_name': self.lower_models_name,
            'lower_model_camel_name': self.lower_model_camel_name,
            'lower_model_name': self.lower_model_name,
            'fields_map': self.model_fields_map,
            'fields_translate_map': dict(zip(self.model_admin.model_fields, self.model_admin.model_translate_fields)),
            'cls': self,
            'db_name': self.db_name,
            'db_user': self.db_user,
            'db_pswd': self.db_pswd,
            'db_field_count': self.db_field_count,
            'db_field_values': self.db_field_values,
            'db_first_id': self.db_first_id,
            'db_last_id': self.db_last_id,
        }
        model_admin_context = {}
        for k in self.model_admin_fields:
            k_value = getattr(self.model_admin, k)
            model_admin_context[k] = k_value

            if k.endswith('_fields'):
                model_admin_context[f"{k}_type_map"] = {k1: v1 for k1, v1 in self.model_fields_map.items() if
                                                        k1 in k_value}
            if k.endswith('_restraint'):
                model_admin_context[f"{k}_translate"] = [base_context['fields_translate_map'][v] for v in k_value]
                model_admin_context[f"{k}_type_map"] = {v: self.model_fields_map[v]
                                                        for v in k_value}

        context = base_context | model_admin_context
        return context

    def build_query_params(self):
        context = self._build_context()
        params_list = [f"query{FieldUtil.snake_to_camel(f)}" for f in context['list_filter_fields_type_map'].keys()]
        return ', '.join(params_list)

    def _to_test_folder(self):
        """Copy all files to test folder"""
        shutil.copytree(str(self.output_angular_dir), "W:/projects/work/ForCodeGen/src/app/game", dirs_exist_ok=True)
        shutil.copytree(str(self.out_rust_dir), "W:/rustProjects/web-base", dirs_exist_ok=True)


@dataclass
class AngularModelRegister(ModelRegister):
    """"""

    def gen_a_interface(self):
        template = 'interfaces.jinja'
        target = f"{self.lower_model_name}/{self.lower_model_name}_interfaces.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_b_api(self):
        template = 'api.jinja'
        target = f"{self.lower_model_name}/{self.lower_model_name}_api.service.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_b1_api_spec(self):
        template = 'api.spec.jinja'
        target = f"{self.lower_model_name}/{self.lower_model_name}_api.service.spec.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_c_module(self):
        template = 'module.jinja'
        target = f"{self.app_name}.module.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_d_router(self):
        template = 'routers.jinja'
        target = f"{self.app_name}-routing.module.ts"
        self._draw_template(template_name=template, target=target, project='angular')

    def gen_e_app_components(self):
        components = ['dashboard']
        for component in components:
            self._draw_component(component_name=component, level='app')

    def gen_e_model_components(self):
        components = ['list', 'creator', 'updater']
        for component in components:
            self._draw_component(component_name=component, level='model_pos')


@dataclass
class RustModelRegister(ModelRegister):
    """"""

    def gen_f_rust_project_files(self):
        """Generate rust project root files"""
        rust_template_dir = Path(TEMPLATE_DIR) / BACKEND_TEMPLATE_DIR
        for file_or_dir in rust_template_dir.rglob('*'):
            if file_or_dir.is_file():
                new_f_or_d = Path(str(file_or_dir).replace('model_pos', self.lower_model_name))
                template_path = file_or_dir.relative_to(TEMPLATE_DIR)
                target_path = new_f_or_d.relative_to(rust_template_dir)
                template_name = f"{template_path.parent / template_path.name}".replace('\\', '/')
                self._draw_template(
                    template_name=template_name,
                    target=str(target_path.parent / target_path.stem), project=BACKEND_TEMPLATE_DIR
                )


def generate_whole_app(app_name: str, app_readable_name: str, model: BaseModel, model_admin: ModelAdmin,
                       db_name: str = 'test', db_user: str = 'test', db_pswd: str = 'test'):
    """generate whole app"""
    amr = AngularModelRegister(model_admin=model_admin, model=model, app_name=app_name,
                               app_readable_name=app_readable_name, db_name=db_name, db_user=db_user, db_pswd=db_pswd)
    amr.register()
    rmr = RustModelRegister(model_admin=model_admin, model=model, app_name=app_name,
                            app_readable_name=app_readable_name, db_name=db_name, db_user=db_user, db_pswd=db_pswd)
    rmr.register()

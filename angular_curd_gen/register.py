from dataclasses import dataclass
from pathlib import Path

import inflect
from jinja2 import FileSystemLoader, Environment
from parse import parse
from pydantic import BaseModel

from angular_curd_gen.config import TEMPLATE_DIR


class ModelAdmin:
    model_fields = ()  # base fields for model
    list_display_restraint = ()  # show in list page, only restraint, not need interface
    list_editable_restraint = ()  # can edit in list page, only restraint, not need interface
    model_edit_fields = ()  # can edit in detail page
    model_create_fields = ()  # can create in create page


@dataclass
class ModelRegister:
    """"""
    model_admin: ModelAdmin = None
    model: BaseModel = None
    app_name: str = ''  # app name

    # extract model info
    model_name = ''  # is single
    models_name = ''  # is plural
    lower_model_name = ''
    lower_models_name = ''
    model_fields_map = None  # all model fields with type dict[str,type]
    jinja_env = None
    output_model_dir = ''

    # extract model admin info
    model_admin_fields = ()

    def register(self):
        """run all"""
        self._prepare()
        gen_functions = [i for i in dir(self) if i.startswith('gen_')]
        for f in gen_functions:
            getattr(self, f)()

    def _prepare(self):
        # model
        engine = inflect.engine()

        self.model_name = engine.singular_noun(self.model.__name__) or self.model.__name__
        self.models_name = engine.plural(self.model_name)

        print(f"{self.model_name=} {self.models_name=}")

        self.lower_model_name = self.model_name.lower()
        self.lower_models_name = self.models_name.lower()

        self.model_fields_map = self.model.__dict__['__annotations__']

        # model admin
        self.model_admin_fields = tuple([i for i in dir(self.model_admin) if not i.startswith('_')])

        # template
        loader = FileSystemLoader(TEMPLATE_DIR)
        self.jinja_env = Environment(loader=loader)
        self.output_model_dir = Path(f"output/{self.model_name}")
        self.output_model_dir.mkdir(parents=True, exist_ok=True)

    def _load_template(self, name: str):
        return self.jinja_env.get_template(name)

    def gen_a_interface(self):
        template = 'interfaces.jinja'
        target = f"{self.lower_model_name}_interfaces.ts"
        self._draw_template(template_name=template, target=target)

    def gen_b_api(self):
        template = 'api.jinja'
        target = f"{self.lower_model_name}_api.service.ts"
        self._draw_template(template_name=template, target=target)

    def gen_b1_api_spec(self):
        template = 'api.spec.jinja'
        target = f"{self.lower_model_name}_api.service.spec.ts"
        self._draw_template(template_name=template, target=target)

    def gen_c_list(self):
        print('gen_c_list')
        pass

    def gen_d_create(self):
        print('gen_d_create')
        pass

    def gen_e_update(self):
        print('gen_e_update')
        pass

    def gen_f_router(self):
        print('gen_f_router')
        pass

    def _draw_template(self, template_name: str, target: str):
        template = self._load_template(template_name)
        context = self._build_context()
        rendered_content = template.render(context)
        output_file = self.output_model_dir / target
        with output_file.open('w') as file:
            file.write(rendered_content)

    @staticmethod
    def map_ts_type(t):
        type_str = parse("<class '{type}'>", str(t))
        if not type_str:  # option
            type_str = parse("typing.Optional[{type}]", str(t))

        the_type = type_str.named['type']

        match the_type:
            case 'int':
                return 'number'
            case 'str':
                return 'string'
            case 'bool':
                return 'boolean'
            case 'float':
                return 'number'
            case 'datetime.datetime':
                return 'Date'
            case _:
                raise ValueError(f"not support type {t}")

    def _build_context(self) -> dict:
        base_context = {
            'app_name': self.app_name,
            'model_name': self.model_name,
            'models_name': self.models_name,
            'lower_models_name': self.lower_models_name,
            'lower_model_name': self.lower_model_name,
            'fields_map': self.model_fields_map,
            'cls': self
        }
        model_admin_context = {}
        for k in self.model_admin_fields:
            if k.endswith('_fields'):
                k_value = getattr(self.model_admin, k)
                print(f"{k=} {k_value=}")
                model_admin_context[f"{k}_map"] = {k1: v1 for k1, v1 in self.model_fields_map.items() if
                                                   k1 in k_value}

        context = base_context | model_admin_context
        print(context)
        return context

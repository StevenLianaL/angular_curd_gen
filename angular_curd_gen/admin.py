class ModelAdmin:
    # model_pos
    model_readable_name = ''  # model_pos readable name, if not, use model_pos name
    # field
    model_fields = ()  # base fields for model_pos
    list_display_restraint = ()  # show in list page, only restraint, not need interface
    list_editable_restraint = ()  # can edit in list page, only restraint, not need interface
    list_filter_fields = ()
    list_sort_fields = ()
    model_edit_fields = ()  # can edit in detail page
    model_create_fields = ()  # can create in create page
    model_translate_fields = ()  # translate model_pos fields to human readable

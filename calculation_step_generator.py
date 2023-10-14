from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader('resources/prompts'))


def generate_calculation_step(template_file_name: str, calculation_detail):
    template = environment.get_template(template_file_name)
    return template.render(detail=calculation_detail)






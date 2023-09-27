from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader('resources/prompts'))


def generate_calculation_step(calculation_detail):
    template = environment.get_template('movesap.jinga2')
    return template.render(detail=calculation_detail)






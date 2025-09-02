from utils.driver_factory import create_driver

def before_all(context):
    context.driver = create_driver()

def after_all(context):
    context.driver.quit()

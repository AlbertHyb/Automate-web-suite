Feature: Validar el escenarios de cine fallidos

  Background:
    Given El usuario accede a la URL del sitio web de cine

  Scenario: Verificar que el botón 'Elige tu cine' despliega opciones al hacer clic
    When el usuario hace clic en el botón "Elige tu cine"
    Then debe mostrarse un menú desplegable

  Scenario: Verificar que el botón de búsqueda despliega el campo de búsqueda
    When el usuario hace clic en el botón de búsqueda
    Then debe mostrarse el campo de búsqueda o resultados
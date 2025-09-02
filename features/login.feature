Feature: Acceso al sitio Fake Cinema

  Scenario: El usuario abre la página principal
    Given que el usuario abre el navegador
    When accede a la página de inicio
    Then la página debería cargar con el título correcto

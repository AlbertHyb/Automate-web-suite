Feature: Comprar boletas de cine para Jurassic World

  Background:
    Given El usuario accede a la URL del sitio web de cine

  Scenario Outline: Flujo completo de compra de entradas de cine
    When el usuario selecciona la pelicula "<name>"
    And el usuario selecciona la fecha actual
    And el usuario selecciona un horario disponible
    And el usuario selecciona los asientos de la fila "<fila>" con numeros <numeros>
    And el usuario da clic en comprar boletos
    And el usuario ingresa la cantidad de persona "<cantidadGente>"
    And el usuario procede al pago
    Then el pago debe completarse exitosamente


    Examples:
      | name        | fila | numeros | cantidadGente |
      | Toy Story   | H    | 2,4,5   |  1,2,0        |
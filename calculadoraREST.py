#!/usr/bin/python
import webapp

#USAGE:
# 1. GET http://localhost:1234/
#   - Devuelve el resultado de la operacion si los datos se han introducido
#   - Si no se han introducido informa de que no tiene datos almacenados
# 2. PUT http://localhost:1234/operacion
#   - Guarda los datos introducidos en el body
#   - Los datos en el body se guardan de la siguiente forma:
#   - num1,operacion,num2  (operacion: suma, resta, mult, div)


class calculadora(webapp.webApp):

    result = ""

    def parse (self, request):

        method = request.split(' ',1)[0]
        resource = request.split(' ',2)[1]
        body = request.split('\r\n\r\n',1)[1]

        return method, resource, body


    def process (self, parsedRequest):

        method, resource, body = parsedRequest # ('GET', '/', '')

        if method == "GET":

            if self.result == "":
                htmlAnswer = "No hay ninguna operacion almacenada!"
                httpCode = "200 OK"
            else:
                htmlAnswer = "El resultado de tu operacion es: " + str(self.result)
                httpCode = "200 OK"



        elif method == "PUT" and resource == "/operacion":

            #si tiene el cuerpo con datos almaceno la operacion
            #si no hay datos en el cuerpo, devuelvo error

            if body == "":

                htmlAnswer = "Cuerpo vacio sin datos para operar"
                httpCode = "400 Error"

            else:

                try:
                    num1 = int(body.split(",")[0])
                    ope = body.split(",")[1]
                    num2 = int(body.split(",")[2])

                    htmlAnswer = "Guardada nueva operacion: "
                    httpCode = "200 OK"

                    if ope == 'suma':
                        htmlAnswer += str(num1) + '+' + str(num2)
                        self.result = num1 + num2
                    if ope == 'resta':
                        htmlAnswer += str(num1) + '-' + str(num2)
                        self.result = num1 - num2
                    if ope == 'mult':
                        htmlAnswer += str(num1) + '*' + str(num2)
                        self.result = num1 * num2
                    if ope == 'div':
                        if num2 == 0:
                            htmlAnswer += str(num1) + '/' + str(num2)
                            htmlAnswer += "\r\nOperacion eliminada, no se puede dividir por 0."
                            httpCode = "400 Error"
                            self.result = ""
                        else:
                            htmlAnswer += str(num1) + '/' + str(num2)
                            self.result = num1 / num2
                except:
                    htmlAnswer = "Datos mal introducidos en el cuerpo"
                    htmlAnswer += "\r\nUSAGE: http://localhost:1234/operacion\r\n"
                    htmlAnswer += "\tBody: 45,suma,56"
                    httpCode = "400 Error"
        else:
            htmlAnswer = "USAGE: http://localhost:1234/operacion\r\n"
            htmlAnswer += "\tBody: 45,suma,56"
            httpCode = "400 Error"

        return httpCode, htmlAnswer

if __name__ == "__main__":
    main = calculadora("localhost", 1234)

# RVS task 2

Documentation: https://documenter.getpostman.com/view/14709532/TWDamFaP

Получение всех чисел:
curl --location --request GET 'http://node-14.fergus.host/api/nums'

Отправка числа:
curl --location --request POST 'http://node-14.fergus.host/api/n' \
--header 'Content-Type: application/json' \
--data-raw '{"number":120}'

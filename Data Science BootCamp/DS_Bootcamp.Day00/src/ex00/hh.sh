#!/bin/sh
read v_name
curl "https://api.hh.ru/vacancies?text=$v_name&search_field=name&per_page=20" | jq . > hh.json

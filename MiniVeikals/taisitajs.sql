SELECT "products".*,
       "taisitajs"."name" AS "taisitajss"
FROM "products"
LEFT JOIN "taisitajs" ON "products"."taisitajs" = "taisitajs"."id"
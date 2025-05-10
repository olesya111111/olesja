SELECT
    "products".*,
    "taisitajs"."name" AS "taisitajs"
FROM       
    "products"
    LEFT JOIN "taisitajs" ON "products"."taisitajs_id" = "taisitajs"."id"
SELECT
    "products".*,
    "daudzums"."name" AS "daudzums"
FROM       
    "products"
    LEFT JOIN "daudzums" ON "products"."daudzums_id" = "daudzums"."id"   
SELECT
    "products".*,
    "zimols"."name" AS "zimols"
FROM       
    "products"
    LEFT JOIN "zimols" ON "products"."zimols_id" = "zimols"."id"
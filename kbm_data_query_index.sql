
SELECT "Knowledge".id AS "Knowledge_id", "Knowledge".title AS "Knowledge_title", "Knowledge".description AS "Knowledge_description", "Knowledge".create_at AS "Knowledge_create_at", "Knowledge".create_by AS "Knowledge_create_by", "Knowledge".priority AS "Knowledge_priority" FROM "Knowledge" WHERE ("Knowledge".description @@ plainto_tsquery('python') AND "Knowledge".title @@ plainto_tsquery('python')) OR ("Knowledge".description @@ plainto_tsquery('microsoft') AND "Knowledge".title @@ plainto_tsquery('microsoft')) AND NOT ("Knowledge".description @@ plainto_tsquery('facebook') AND "Knowledge".title @@ plainto_tsquery('facebook'));

SELECT * FROM "Knowledge" WHERE ("Knowledge".description @@ plainto_tsquery('microsft') OR "Knowledge".title @@ plainto_tsquery('microsft') OR "Knowledge".description @@ plainto_tsquery ('python') OR "Knowledge".title @@ plainto_tsquery('python')) AND NOT ("Knowledge".description @@ plainto_tsquery('facebook') OR "Knowledge".title @@ plainto_tsquery('facebook'));

SELECT * FROM "Knowledge" WHERE (("Knowledge".description @@ plainto_tsquery('facebook') OR  "Knowledge".title @@ plainto_tsquery('facebook')) OR ("Knowledge".description @@ plainto_tsquery ('python') OR "Knowledge".title @@ plainto_tsquery('python')) AND NOT ("Knowledge".description @@ plainto_tsquery('microsoft') OR "Knowledge".title @@ plainto_tsquery('microsoft')));

SELECT * FROM "Knowledge" WHERE (("Knowledge".description @@ plainto_tsquery('facebook') OR "Knowledge".title @@ plainto_tsquery('facebook')) AND ("Knowledge".description @@ plainto_tsquery  ('microsoft') OR "Knowledge".title @@ plainto_tsquery('microsoft'))) AND NOT  ("Knowledge".description @@ plainto_tsquery('python') OR "Knowledge".title @@ plainto_tsquery ('python'));


SELECT * FROM "Knowledge" WHERE (("Knowledge".description @@ plainto_tsquery('facebook') OR "Knowledge".title @@ plainto_tsquery('facebook')) AND ("Knowledge".description @@  plainto_tsquery('microsoft') OR "Knowledge".title @@ plainto_tsquery('microsoft'))) AND NOT ("Knowledge".description @@ plainto_tsquery('python') OR "Knowledge".title @@ plainto_tsquery ('python'));

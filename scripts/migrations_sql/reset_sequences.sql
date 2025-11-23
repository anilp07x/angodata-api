
-- Reset auto-increment sequences
SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1));
SELECT setval('provinces_id_seq', COALESCE((SELECT MAX(id) FROM provinces), 1));
SELECT setval('municipalities_id_seq', COALESCE((SELECT MAX(id) FROM municipalities), 1));
SELECT setval('schools_id_seq', COALESCE((SELECT MAX(id) FROM schools), 1));
SELECT setval('markets_id_seq', COALESCE((SELECT MAX(id) FROM markets), 1));
SELECT setval('hospitals_id_seq', COALESCE((SELECT MAX(id) FROM hospitals), 1));

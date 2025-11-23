INSERT INTO users (id, username, email, password_hash, role, created_at)
VALUES (1, 'Anilson Pedro', 'anilpedro07@gmail.com', 
        '$2b$12$6vmZh/OB4wDWY2uxbSGyde4F5Njf1tRicwm0sUXzDCrH72v77rsRW', 'admin', '2025-11-21T19:19:57.147253')
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, username, email, password_hash, role, created_at)
VALUES (2, 'João Silva', 'joao@example.com', 
        '$2b$12$7i7MwgtJlsj009nFJ/AdeOIBYGNz0xNRbGdaWBaC.rO69Q6lFtoo6', 'editor', '2025-11-21T20:53:55.595114')
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, username, email, password_hash, role, created_at)
VALUES (3, 'User Test', 'user@example.com', 
        '$2b$12$6Bb9Xfe6WthLZ2a7.57iluRfUYEc0SPS.IlDMg6qFrcNVDGup0RM.', 'user', '2025-11-21T22:17:29.715500')
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, username, email, password_hash, role, created_at)
VALUES (4, 'Admin Teste', 'admin@teste.com', 
        '$2b$12$29HNxS6GU7CeCWcKeUkFV.ImODWCtFwUQnctpNx8oMFyqpLeOAIpO', 'admin', '2025-11-23T11:20:27.992667')
ON CONFLICT (email) DO NOTHING;

INSERT INTO users (id, username, email, password_hash, role, created_at)
VALUES (5, 'Editor Teste', 'editor@teste.com', 
        '$2b$12$skxvUWlRwC7KNdRHSkmqTO2mI8bhMCyvRobrNsuLMhTTEMJ3AaPoy', 'editor', '2025-11-23T11:24:19.899956')
ON CONFLICT (email) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (1, 'Luanda', 'Ingombota', 
        18826, 6945386)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (2, 'Bengo', 'Dande', 
        31371, 356641)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (3, 'Benguela', 'Benguela', 
        39826, 2231385)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (4, 'Bié', 'Cuito', 
        70314, 1455255)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (5, 'Cabinda', 'Cabinda', 
        7270, 716076)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (6, 'Cuando', 'Mavinga', 
        95000, 250000)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (7, 'Cubango', 'Menongue', 
        104049, 284002)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (8, 'Cuanza Norte', 'Cazengo', 
        24110, 443386)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (9, 'Cuanza Sul', 'Sumbe', 
        55660, 1881873)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (10, 'Cunene', 'Cuanhama', 
        78342, 990087)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (11, 'Huambo', 'Huambo', 
        34274, 2019555)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (12, 'Huíla', 'Lubango', 
        79023, 2497422)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (13, 'Lunda Norte', 'Dundo', 
        103760, 862566)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (14, 'Lunda Sul', 'Saurimo', 
        77637, 537587)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (15, 'Malanje', 'Malanje', 
        97602, 986363)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (16, 'Moxico', 'Luena', 
        113023, 578568)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (17, 'Moxico Leste', 'Cazombo', 
        110000, 180000)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (18, 'Namibe', 'Moçâmedes', 
        58137, 495326)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (19, 'Uíge', 'Uíge', 
        58698, 1483118)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (20, 'Zaire', 'Mbanza Kongo', 
        40130, 594428)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES (21, 'Icolo e Bengo', 'Catete', 
        3800, 180000)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (1, 'Belas', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (2, 'Cacuaco', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (3, 'Cazenga', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (4, 'Kilamba Kiaxi', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (5, 'Viana', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (6, 'Mussulo', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (7, 'Sambizanga', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (8, 'Rangel', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (9, 'Maianga', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (10, 'Samba', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (11, 'Camama', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (12, 'Mulenvos', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (13, 'Kilamba', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (14, 'Hoji Ya Henda', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (15, 'Ingombota', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (16, 'Talatona', 1, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (17, 'Bula Atumba', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (18, 'Dande', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (19, 'Quibaxe', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (20, 'Nambuangongo', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (21, 'Pango Aluquém', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (22, 'Ambriz', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (23, 'Muxaluando', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (24, 'Piri', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (25, 'Quicunzo', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (26, 'Úcua', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (27, 'Panguila', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (28, 'Barra do Dande', 2, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (29, 'Baía Farta', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (30, 'Balombo', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (31, 'Bocoio', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (32, 'Caimbambo', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (33, 'Catumbela', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (34, 'Chongorói', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (35, 'Cubal', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (36, 'Ganda', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (37, 'Lobito', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (38, 'Benguela', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (39, 'Egito Praia', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (40, 'Chindumbo', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (41, 'Dombe Grande', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (42, 'Capupa', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (43, 'Biópio', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (44, 'Chila', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (45, 'Chicuma', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (46, 'Babaera', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (47, 'Iambala', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (48, 'Catengue', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (49, 'Bolonguera', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (50, 'Canhamela', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (51, 'Navegantes', 3, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (52, 'Andulo', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (53, 'Camacupa', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (54, 'Catabola', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (55, 'Chinguar', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (56, 'Chitembo', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (57, 'Cuemba', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (58, 'Cuito', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (59, 'Cunhinga', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (60, 'Nharêa', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (61, 'Luando', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (62, 'Ringoma', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (63, 'Mumbué', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (64, 'Calucinga', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (65, 'Chicala', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (66, 'Chipeta', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (67, 'Umpulo', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (68, 'Lúbia', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (69, 'Cambândua', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (70, 'Belo Horizonte', 4, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (71, 'Belize', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (72, 'Buco-Zau', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (73, 'Cabinda', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (74, 'Cacongo', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (75, 'Miconje', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (76, 'Massabi', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (77, 'Necuto', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (78, 'Tando Zinze', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (79, 'Liambo', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (80, 'Ngoio', 5, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (81, 'Cuito Cuanavale', 6, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (82, 'Dirico', 6, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (83, 'Mavinga', 6, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (84, 'Rivungo', 6, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (85, 'Xipundo', 6, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (86, 'Dima', 6, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (87, 'Luiana', 6, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (88, 'Mucusso', 6, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (89, 'Luengue', 6, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (90, 'Calai', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (91, 'Cuangar', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (92, 'Cuchi', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (93, 'Cutato', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (94, 'Caiundo', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (95, 'Longa', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (96, 'Menongue', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (97, 'Nancova', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (98, 'Savate', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (99, 'Chinguanja', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (100, 'Mavengue', 7, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (101, 'Ambaca', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (102, 'Banga', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (103, 'Bolongongo', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (104, 'Cambambe', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (105, 'Cazengo', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (106, 'Golungo Alto', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (107, 'Lucala', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (108, 'Ngonguembo', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (109, 'Quiculungo', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (110, 'Samba Cajú', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (111, 'Massangano', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (112, 'Cêrca', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (113, 'Tango', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (114, 'Terreiro', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (115, 'Aldeia Nova', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (116, 'Caculo Cabaça', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (117, 'Luinga', 8, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (118, 'Gabela', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (119, 'Cassongue', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (120, 'Waku Kungo', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (121, 'Conda', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (122, 'Ebo', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (123, 'Calulo', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (124, 'Mussende', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (125, 'Porto Amboim', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (126, 'Quibala', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (127, 'Quilenda', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (128, 'Seles', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (129, 'Sumbe', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (130, 'Quirimbo', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (131, 'Munenga', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (132, 'Quissongo', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (133, 'Gungo', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (134, 'Sanga', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (135, 'Gangula', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (136, 'Pambangala', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (137, 'Condé', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (138, 'Amboiva', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (139, 'Lonhe', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (140, 'Quenha', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (141, 'Boa Entrada', 9, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (142, 'Cahama', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (143, 'Cuanhama', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (144, 'Curoca', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (145, 'Cuvelai', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (146, 'Namacunde', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (147, 'Ombandja', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (148, 'Chiéde', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (149, 'Nehone', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (150, 'Humbe', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (151, 'Mupa', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (152, 'Naulila', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (153, 'Chitado', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (154, 'Cafima', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (155, 'Chissuata', 10, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (156, 'Bailundo', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (157, 'Caála', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (158, 'Cachiungo', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (159, 'Chicala', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (160, 'Chinjenje', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (161, 'Ecunha', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (162, 'Huambo', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (163, 'Londuimbali', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (164, 'Longonjo', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (165, 'Mungo', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (166, 'Ucuma', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (167, 'Bimbe', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (168, 'Sambo', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (169, 'Galanga', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (170, 'Alto Hama', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (171, 'Chilata', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (172, 'Cuima', 11, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (173, 'Caconda', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (174, 'Cacula', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (175, 'Caluquembe', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (176, 'Chibia', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (177, 'Chicomba', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (178, 'Chipindo', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (179, 'Cuvango', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (180, 'Gambos', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (181, 'Humpata', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (182, 'Jamba Mineira', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (183, 'Lubango', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (184, 'Matala', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (185, 'Quilengues', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (186, 'Quipungo', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (187, 'Dongo', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (188, 'António Kahala', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (189, 'Hoque', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (190, 'Capelongo', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (191, 'Chituto', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (192, 'Capunda Cavilongo', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (193, 'Viti Vivali', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (194, 'Galangue', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (195, 'Palanca', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (196, 'Chicungo', 12, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (197, 'Cambulo', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (198, 'Capenda Camulemba', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (199, 'Caungula', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (200, 'Chitato', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (201, 'Cuango', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (202, 'Cuílo', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (203, 'Lubalo', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (204, 'Lucapa', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (205, 'Lóvua', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (206, 'Xá-Muteba', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (207, 'Dundo', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (208, 'Xá Cassau', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (209, 'Camaxilo', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (210, 'Luangue', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (211, 'Luremo', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (212, 'Canzar', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (213, 'Cassanje Calucala', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (214, 'Mussungue', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (215, 'Cafunfu', 13, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (216, 'Cacolo', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (217, 'Dala', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (218, 'Muconda', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (219, 'Saurimo', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (220, 'Chiluage', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (221, 'Cassai-Sul', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (222, 'Xassengue', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (223, 'Alto Chicapa', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (224, 'Sombo', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (225, 'Muriege', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (226, 'Luma Cassai', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (227, 'Cazage', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (228, 'Muangueji', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (229, 'Cassengo', 14, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (230, 'Cacuso', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (231, 'Cahombo', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (232, 'Calandula', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (233, 'Cambundi Catembo', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (234, 'Cangandala', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (235, 'Kiwaba Nzoji', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (236, 'Kunda Dya Baze', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (237, 'Luquembo', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (238, 'Malanje', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (239, 'Marimba', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (240, 'Massango', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (241, 'Quela', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (242, 'Quirima', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (243, 'Cateco Cangola', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (244, 'Cuale', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (245, 'Pungo A Ndongo', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (246, 'Ngola Luiji', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (247, 'Quihuhu', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (248, 'Xandel', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (249, 'Cambo Suinginge', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (250, 'Milando', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (251, 'Quitapa', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (252, 'Capunda', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (253, 'Muquixe', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (254, 'Quêssua', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (255, 'Caculama', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (256, 'Mbanji Ya Ngola', 15, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (257, 'Chiúme', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (258, 'Lumbala Nguimbo', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (259, 'Camanongue', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (260, 'Léua', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (261, 'Lutembo', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (262, 'Cangumbe', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (263, 'Luena', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (264, 'Cangamba', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (265, 'Lucusse', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (266, 'Ninda', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (267, 'Lutuai', 16, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (268, 'Cazombo', 17, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (269, 'Luacano', 17, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (270, 'Cameia', 17, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (271, 'Luau', 17, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (272, 'Nana Candundo', 17, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (273, 'Macondo', 17, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (274, 'Caianda', 17, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (275, 'Lóvua do Zambeze', 17, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (276, 'Lago Dilolo', 17, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (277, 'Moçâmedes', 18, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (278, 'Camucuio', 18, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (279, 'Bibala', 18, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (280, 'Virei', 18, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (281, 'Tômbua', 18, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (282, 'Lucira', 18, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (283, 'Iona', 18, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (284, 'Sacomar', 18, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (285, 'Cacimbas', 18, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (286, 'Uíge', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (287, 'Cangola', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (288, 'Ambuíla', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (289, 'Bembe', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (290, 'Nova Esperança', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (291, 'Bungo', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (292, 'Milunga', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (293, 'Damba', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (294, 'Maquela do Zombo', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (295, 'Mucaba', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (296, 'Negage', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (297, 'Puri', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (298, 'Quimbele', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (299, 'Dange Quitexe', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (300, 'Sanza Pombo', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (301, 'Songo', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (302, 'Sacandica', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (303, 'Nsosso', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (304, 'Lucunga', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (305, 'Quipedro', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (306, 'Massau', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (307, 'Vista Alegre', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (308, 'Alto Zaza', 19, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (309, 'Mbanza Kongo', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (310, 'Soyo', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (311, 'Nzeto', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (312, 'Cuimba', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (313, 'Nóqui', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (314, 'Tomboco', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (315, 'Luvo', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (316, 'Lufico', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (317, 'Quêlo', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (318, 'Serra de Canda', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (319, 'Quindeje', 20, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (320, 'Catete', 21, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (321, 'Quiçama', 21, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (322, 'Calumbo', 21, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (323, 'Cabiri', 21, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (324, 'Cabo Ledo', 21, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (325, 'Bom Jesus', 21, 
        NULL, NULL);

INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES (326, 'Sequele', 21, 
        NULL, NULL);

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (1, 'Escola Secundária Mutu Ya Kevela', 1, 
        'Maianga', 
        'Pública', 
        '');

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (2, 'Colégio São Francisco de Assis', 1, 
        'Talatona', 
        'Privada', 
        '');

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (3, 'Instituto Médio Politécnico do Cazenga', 1, 
        'Cazenga', 
        'Pública', 
        '');

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (4, 'Escola Secundária Comandante Gika', 3, 
        'Benguela', 
        'Pública', 
        '');

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (5, 'Escola do II Ciclo do Ensino Secundário do Lobito', 3, 
        'Lobito', 
        'Pública', 
        '');

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (6, 'Instituto Médio de Economia do Huambo', 11, 
        'Huambo', 
        'Pública', 
        '');

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (7, 'Escola Secundária da Tchivinguiro', 12, 
        'Lubango', 
        'Pública', 
        '');

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (8, 'Colégio Ekuikui II', 12, 
        'Lubango', 
        'Privada', 
        '');

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (9, 'Escola Teste', 1, 
        'Belas', 
        'Pública', 
        '');

INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES (10, 'Escola Editor', 1, 
        'Belas', 
        'Pública', 
        '');

INSERT INTO markets (id, nome, provincia_id, municipio, tipo, endereco)
VALUES (1, 'Mercado do Roque Santeiro', 1, 
        'Cacuaco', 
        'Informal', 
        '');

INSERT INTO markets (id, nome, provincia_id, municipio, tipo, endereco)
VALUES (2, 'Mercado dos Kwanzas', 1, 
        'Maianga', 
        'Formal', 
        '');

INSERT INTO markets (id, nome, provincia_id, municipio, tipo, endereco)
VALUES (3, 'Mercado do Cazenga', 1, 
        'Cazenga', 
        'Informal', 
        '');

INSERT INTO markets (id, nome, provincia_id, municipio, tipo, endereco)
VALUES (4, 'Mercado da Catumbela', 3, 
        'Catumbela', 
        'Municipal', 
        '');

INSERT INTO markets (id, nome, provincia_id, municipio, tipo, endereco)
VALUES (5, 'Mercado Central do Lobito', 3, 
        'Lobito', 
        'Municipal', 
        '');

INSERT INTO markets (id, nome, provincia_id, municipio, tipo, endereco)
VALUES (6, 'Mercado do Huambo', 11, 
        'Huambo', 
        'Municipal', 
        '');

INSERT INTO markets (id, nome, provincia_id, municipio, tipo, endereco)
VALUES (7, 'Mercado da Tchavola', 12, 
        'Lubango', 
        'Informal', 
        '');

INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (1, 'Hospital Américo Boavida', 1, 
        'Maianga', 
        'Público', 
        'Maianga', 
        '');

INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (2, 'Hospital Josina Machel', 1, 
        'Samba', 
        'Público', 
        'Samba', 
        '');

INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (3, 'Clínica Girassol', 1, 
        'Talatona', 
        'Privado', 
        'Talatona', 
        '');

INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (4, 'Hospital Provincial do Bengo', 2, 
        'Dande', 
        'Público', 
        'Centro', 
        '');

INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (5, 'Hospital ProvinINSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (5, 'Hospital Provincial de Benguela', 3, 
        'Benguela', 
        'Público', 
        'Centro', 
        '');
INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (6, 'Hospital Municipal do Lobito', 3, 
        'Lobito', 
        'Público', 
        'Centro', 
        '');
INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (7, 'Hospital Central do Huambo', 11, 
        'Huambo', 
        'Público', 
        'Centro', 
        '');
INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (8, 'Hospital Central da Huíla', 12, 
        'Lubango', 
        'Público', 
        'Centro', 
        '');
INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES (9, 'Hospital Pediátrico David Bernardino', 1, 
        'Rangel', 
        'Público', 
        'Sambizanga', 
        '');

-- RESET SEQUENCES

-- Reset auto-increment sequences to continue from max ID
SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1));
SELECT setval('provinces_id_seq', COALESCE((SELECT MAX(id) FROM provinces), 1));
SELECT setval('municipalities_id_seq', COALESCE((SELECT MAX(id) FROM municipalities), 1));
SELECT setval('schools_id_seq', COALESCE((SELECT MAX(id) FROM schools), 1));
SELECT setval('markets_id_seq', COALESCE((SELECT MAX(id) FROM markets), 1));
SELECT setval('hospitals_id_seq', COALESCE((SELECT MAX(id) FROM hospitals), 1));


✅ SQL salvo em: /home/server-dev/projects/angodata-api/scripts/migration.sql

📋 Para executar:
   1. Copie o SQL acima
   2. Cole no Supabase SQL Editor
   3. Execute
   OU execute: cat /home/server-dev/projects/angodata-api/scripts/migration.sql | supabase db execute

======================================================================
MIGRAÇÃO COMPLETA!
======================================================================

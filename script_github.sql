--
-- PostgreSQL database dump
--

\restrict QuP2ddYruifDccuhxqOmR9tTdBuJFcKSkNQIaltf3fmLNAh5eePPANnpxTYfaau

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: update_updated_at(); Type: FUNCTION; Schema: public; Owner: diego
--

CREATE FUNCTION public.update_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$;


ALTER FUNCTION public.update_updated_at() OWNER TO diego;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alerts; Type: TABLE; Schema: public; Owner: diego
--

CREATE TABLE public.alerts (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    product_id uuid NOT NULL,
    store_id uuid,
    target_price numeric(12,2) NOT NULL,
    condition character varying(20) DEFAULT 'below'::character varying NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    triggered_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT alerts_condition_valid CHECK (((condition)::text = ANY ((ARRAY['below'::character varying, 'above'::character varying, 'equals'::character varying])::text[]))),
    CONSTRAINT alerts_price_positive CHECK ((target_price >= (0)::numeric))
);


ALTER TABLE public.alerts OWNER TO diego;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: diego
--

CREATE TABLE public.categories (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL,
    description text,
    parent_id uuid,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT categories_name_not_empty CHECK ((char_length((name)::text) > 0))
);


ALTER TABLE public.categories OWNER TO diego;

--
-- Name: price_history; Type: TABLE; Schema: public; Owner: diego
--

CREATE TABLE public.price_history (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    product_store_url_id uuid NOT NULL,
    price numeric(12,2) NOT NULL,
    currency character(3) DEFAULT 'EUR'::bpchar NOT NULL,
    in_stock boolean DEFAULT true NOT NULL,
    scraped_status character varying(50) DEFAULT 'success'::character varying,
    scraped_at timestamp with time zone DEFAULT now(),
    CONSTRAINT price_history_price_positive CHECK ((price >= (0)::numeric))
);


ALTER TABLE public.price_history OWNER TO diego;

--
-- Name: product_store_urls; Type: TABLE; Schema: public; Owner: diego
--

CREATE TABLE public.product_store_urls (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    product_id uuid NOT NULL,
    store_id uuid NOT NULL,
    url text NOT NULL,
    selector_price character varying(255),
    selector_name character varying(255),
    is_active boolean DEFAULT true NOT NULL,
    last_checked timestamp with time zone
);


ALTER TABLE public.product_store_urls OWNER TO diego;

--
-- Name: product_tags; Type: TABLE; Schema: public; Owner: diego
--

CREATE TABLE public.product_tags (
    product_id uuid NOT NULL,
    tag_id uuid NOT NULL
);


ALTER TABLE public.product_tags OWNER TO diego;

--
-- Name: products; Type: TABLE; Schema: public; Owner: diego
--

CREATE TABLE public.products (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    category_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    brand character varying(100),
    image_url text,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.products OWNER TO diego;

--
-- Name: stores; Type: TABLE; Schema: public; Owner: diego
--

CREATE TABLE public.stores (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(100) NOT NULL,
    base_url character varying(255) NOT NULL,
    currency character(3) DEFAULT 'EUR'::bpchar NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.stores OWNER TO diego;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: diego
--

CREATE TABLE public.tags (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    name character varying(50) NOT NULL,
    color character(7) DEFAULT '#6B7280'::bpchar
);


ALTER TABLE public.tags OWNER TO diego;

--
-- Name: v_current_prices; Type: VIEW; Schema: public; Owner: diego
--

CREATE VIEW public.v_current_prices AS
 SELECT DISTINCT ON (psu.id) p.id AS product_id,
    p.name AS product_name,
    s.name AS store_name,
    ph.price,
    ph.currency,
    ph.in_stock,
    ph.scraped_at
   FROM (((public.price_history ph
     JOIN public.product_store_urls psu ON ((ph.product_store_url_id = psu.id)))
     JOIN public.products p ON ((psu.product_id = p.id)))
     JOIN public.stores s ON ((psu.store_id = s.id)))
  ORDER BY psu.id, ph.scraped_at DESC;


ALTER VIEW public.v_current_prices OWNER TO diego;

--
-- Name: v_price_stats; Type: VIEW; Schema: public; Owner: diego
--

CREATE VIEW public.v_price_stats AS
 SELECT p.id AS product_id,
    p.name AS product_name,
    s.name AS store_name,
    min(ph.price) AS price_min,
    max(ph.price) AS price_max,
    round(avg(ph.price), 2) AS price_avg,
    count(*) AS data_points,
    max(ph.scraped_at) AS last_check
   FROM (((public.price_history ph
     JOIN public.product_store_urls psu ON ((ph.product_store_url_id = psu.id)))
     JOIN public.products p ON ((psu.product_id = p.id)))
     JOIN public.stores s ON ((psu.store_id = s.id)))
  WHERE ((ph.scraped_status)::text = 'success'::text)
  GROUP BY p.id, p.name, s.name;


ALTER VIEW public.v_price_stats OWNER TO diego;

--
-- Data for Name: alerts; Type: TABLE DATA; Schema: public; Owner: diego
--

COPY public.alerts (id, product_id, store_id, target_price, condition, is_active, triggered_at, created_at) FROM stdin;
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: diego
--

COPY public.categories (id, name, slug, description, parent_id, created_at) FROM stdin;
faa97a91-6ca0-49b5-a76c-343a4434ba9d	Tecnología	tecnologia	\N	\N	2026-04-28 17:51:06.699037+02
d09531aa-bbd1-45c4-b744-ee103686fc3b	Ropa	ropa	\N	\N	2026-04-28 17:51:06.699037+02
f8cce6ba-52f7-42ee-83f1-f0d8780529bc	Hogar	hogar	\N	\N	2026-04-28 17:51:06.699037+02
d88dc291-e3be-4292-af3e-daa59f290adb	Deportes	deportes	\N	\N	2026-04-28 17:51:06.699037+02
0079df33-1825-4a39-84fa-83b611ecd856	Portátiles	portatiles	\N	faa97a91-6ca0-49b5-a76c-343a4434ba9d	2026-04-28 17:51:06.701778+02
d84aaeef-0db5-4033-a029-661824edb429	Smartphones	smartphones	\N	faa97a91-6ca0-49b5-a76c-343a4434ba9d	2026-04-28 17:51:06.701778+02
d7d372ff-9670-46af-a9cc-e8765155d119	Ropa Hombre	ropa-hombre	\N	d09531aa-bbd1-45c4-b744-ee103686fc3b	2026-04-28 17:51:06.701778+02
47a5276f-72e4-49f7-8559-a2ed0cad2c34	Ropa Mujer	ropa-mujer	\N	d09531aa-bbd1-45c4-b744-ee103686fc3b	2026-04-28 17:51:06.701778+02
\.


--
-- Data for Name: price_history; Type: TABLE DATA; Schema: public; Owner: diego
--

COPY public.price_history (id, product_store_url_id, price, currency, in_stock, scraped_status, scraped_at) FROM stdin;
\.


--
-- Data for Name: product_store_urls; Type: TABLE DATA; Schema: public; Owner: diego
--

COPY public.product_store_urls (id, product_id, store_id, url, selector_price, selector_name, is_active, last_checked) FROM stdin;
\.


--
-- Data for Name: product_tags; Type: TABLE DATA; Schema: public; Owner: diego
--

COPY public.product_tags (product_id, tag_id) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: diego
--

COPY public.products (id, category_id, name, description, brand, image_url, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: stores; Type: TABLE DATA; Schema: public; Owner: diego
--

COPY public.stores (id, name, base_url, currency, is_active, created_at) FROM stdin;
b52d03b5-8490-47ca-b723-efb76cadacdf	Amazon ES	https://www.amazon.es	EUR	t	2026-04-28 17:51:06.709836+02
3be1781a-4569-4d53-a4ea-bc2f62331ed6	PCComponentes	https://www.pccomponentes.com	EUR	t	2026-04-28 17:51:06.709836+02
552b6539-ca86-454a-b3e1-1c9bc7fc85cc	Zara	https://www.zara.com/es	EUR	t	2026-04-28 17:51:06.709836+02
33082a40-6594-4eec-9c66-4c7b497f0d3a	MediaMarkt	https://www.mediamarkt.es	EUR	t	2026-04-28 17:51:06.709836+02
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: diego
--

COPY public.tags (id, name, color) FROM stdin;
\.


--
-- Name: alerts alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: categories categories_slug_key; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_slug_key UNIQUE (slug);


--
-- Name: price_history price_history_pkey; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.price_history
    ADD CONSTRAINT price_history_pkey PRIMARY KEY (id);


--
-- Name: product_store_urls product_store_urls_pkey; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.product_store_urls
    ADD CONSTRAINT product_store_urls_pkey PRIMARY KEY (id);


--
-- Name: product_tags product_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.product_tags
    ADD CONSTRAINT product_tags_pkey PRIMARY KEY (product_id, tag_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: stores stores_name_key; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_name_key UNIQUE (name);


--
-- Name: stores stores_pkey; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (id);


--
-- Name: tags tags_name_key; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_name_key UNIQUE (name);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: product_store_urls uq_product_store; Type: CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.product_store_urls
    ADD CONSTRAINT uq_product_store UNIQUE (product_id, store_id);


--
-- Name: idx_alerts_active; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_alerts_active ON public.alerts USING btree (is_active) WHERE (is_active = true);


--
-- Name: idx_alerts_product; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_alerts_product ON public.alerts USING btree (product_id);


--
-- Name: idx_categories_parent; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_categories_parent ON public.categories USING btree (parent_id);


--
-- Name: idx_categories_slug; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_categories_slug ON public.categories USING btree (slug);


--
-- Name: idx_ph_psu_time; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_ph_psu_time ON public.price_history USING btree (product_store_url_id, scraped_at DESC);


--
-- Name: idx_ph_scraped_at; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_ph_scraped_at ON public.price_history USING btree (scraped_at DESC);


--
-- Name: idx_ph_status; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_ph_status ON public.price_history USING btree (scraped_status);


--
-- Name: idx_products_active; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_products_active ON public.products USING btree (is_active);


--
-- Name: idx_products_brand; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_products_brand ON public.products USING btree (brand);


--
-- Name: idx_products_category; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_products_category ON public.products USING btree (category_id);


--
-- Name: idx_products_name_trgm; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_products_name_trgm ON public.products USING gin (name public.gin_trgm_ops);


--
-- Name: idx_psu_active; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_psu_active ON public.product_store_urls USING btree (is_active);


--
-- Name: idx_psu_product; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_psu_product ON public.product_store_urls USING btree (product_id);


--
-- Name: idx_psu_store; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_psu_store ON public.product_store_urls USING btree (store_id);


--
-- Name: idx_stores_active; Type: INDEX; Schema: public; Owner: diego
--

CREATE INDEX idx_stores_active ON public.stores USING btree (is_active);


--
-- Name: products trg_products_updated_at; Type: TRIGGER; Schema: public; Owner: diego
--

CREATE TRIGGER trg_products_updated_at BEFORE UPDATE ON public.products FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();


--
-- Name: alerts alerts_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: alerts alerts_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE SET NULL;


--
-- Name: categories categories_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- Name: price_history price_history_product_store_url_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.price_history
    ADD CONSTRAINT price_history_product_store_url_id_fkey FOREIGN KEY (product_store_url_id) REFERENCES public.product_store_urls(id) ON DELETE CASCADE;


--
-- Name: product_store_urls product_store_urls_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.product_store_urls
    ADD CONSTRAINT product_store_urls_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: product_store_urls product_store_urls_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.product_store_urls
    ADD CONSTRAINT product_store_urls_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE CASCADE;


--
-- Name: product_tags product_tags_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.product_tags
    ADD CONSTRAINT product_tags_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: product_tags product_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.product_tags
    ADD CONSTRAINT product_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diego
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE RESTRICT;


--
-- PostgreSQL database dump complete
--

\unrestrict QuP2ddYruifDccuhxqOmR9tTdBuJFcKSkNQIaltf3fmLNAh5eePPANnpxTYfaau


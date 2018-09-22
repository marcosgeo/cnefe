--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.9
-- Dumped by pg_dump version 9.6.9

-- Started on 2018-08-10 21:18:54 -03

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 9 (class 2615 OID 19500)
-- Name: censo2010; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA censo2010;


--
-- TOC entry 1404 (class 1255 OID 19501)
-- Name: cnefe_enderecos_create_ordem(); Type: FUNCTION; Schema: censo2010; Owner: -
--

CREATE FUNCTION censo2010.cnefe_enderecos_create_ordem() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
    if (NEW.ordem is null or NEW.ordem = 0) then
	update censo2010.cnefe_enderecos set ordem = (
		select 
			case when max(ordem) > 0 then max(ordem) + 1 else 1 end  
		from censo2010.cnefe_enderecos
		where setor_id = NEW.setor_id and quadra_num = NEW.quadra_num and face_num = NEW.face_num
	)
	where id=NEW.id;
	return NEW;
    elsif (NEW.ordem > 0) then
	update censo2010.cnefe_enderecos set ordem = ordem + 1 
		where setor_id = NEW.setor_id and quadra_num = NEW.quadra_num and face_num = NEW.face_num 
			and ordem = NEW.ordem and id <> NEW.id;
	return NEW;
    end if;
end;
$$;


--
-- TOC entry 1405 (class 1255 OID 19502)
-- Name: update_ordem(); Type: FUNCTION; Schema: censo2010; Owner: -
--

CREATE FUNCTION censo2010.update_ordem() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin

if OLD.ordem <> NEW.ordem then
	update censo2010.cnefe_enderecos set ordem = ordem + 1 
	where setor_id = NEW.setor_id and quadra_num = NEW.quadra_num 
		and face_num = NEW.face_num and ordem = NEW.ordem and id <> NEW.id;
end if;
return NEW;
end;
$$;


SET default_with_oids = false;

--
-- TOC entry 211 (class 1259 OID 19644)
-- Name: cnefe_enderecos; Type: TABLE; Schema: censo2010; Owner: -
--

CREATE TABLE censo2010.cnefe_enderecos (
    id integer NOT NULL,
    setor_id character varying(16),
    uf_cod character varying(2),
    muni_cod character varying(7),
    distrito character varying(2),
    subdistrito character varying(2),
    setor_cod character varying(4),
    setor_sit character varying(2),
    quadra_num smallint,
    face_num smallint,
    ordem smallint,
    especie character varying(2),
    lograd_tipo character varying(20),
    lograd_tit character varying(30),
    lograd_nome character varying(60),
    imovel_numero integer,
    modificador character varying(10),
    cep character varying(8),
    comp_elem1 character varying(20),
    comp_valor1 character varying(10),
    comp_elem2 character varying(20),
    comp_valor2 character varying(10),
    comp_elem3 character varying(20),
    comp_valor3 character varying(10),
    comp_elem4 character varying(20),
    comp_valor4 character varying(10),
    comp_elem5 character varying(20),
    comp_valor5 character varying(10),
    comp_elem6 character varying(20),
    comp_valor6 character varying(10),
    latitude character varying(15),
    longitude character varying(15),
    localidade character varying(60),
    nome_estab character varying(40),
    indicador character varying(1),
    coletivo character varying(30)
);


--
-- TOC entry 210 (class 1259 OID 19642)
-- Name: cnefe_enderecos_id_seq; Type: SEQUENCE; Schema: censo2010; Owner: -
--

CREATE SEQUENCE censo2010.cnefe_enderecos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3616 (class 0 OID 0)
-- Dependencies: 210
-- Name: cnefe_enderecos_id_seq; Type: SEQUENCE OWNED BY; Schema: censo2010; Owner: -
--

ALTER SEQUENCE censo2010.cnefe_enderecos_id_seq OWNED BY censo2010.cnefe_enderecos.id;


--
-- TOC entry 202 (class 1259 OID 19511)
-- Name: cnefe_faces; Type: TABLE; Schema: censo2010; Owner: -
--

CREATE TABLE censo2010.cnefe_faces (
    gid integer NOT NULL,
    geom public.geometry(LineString,4674),
    id integer,
    codigo character varying(24),
    setor character varying(16),
    quadra smallint,
    face smallint,
    lograd_tipo character varying(20),
    lograd_titulo character varying(30),
    lograd_nome character varying(60),
    residencias smallint,
    imoveis smallint,
    tipo character varying(10)
);


--
-- TOC entry 203 (class 1259 OID 19517)
-- Name: cnefe_faces_gid_seq; Type: SEQUENCE; Schema: censo2010; Owner: -
--

CREATE SEQUENCE censo2010.cnefe_faces_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3617 (class 0 OID 0)
-- Dependencies: 203
-- Name: cnefe_faces_gid_seq; Type: SEQUENCE OWNED BY; Schema: censo2010; Owner: -
--

ALTER SEQUENCE censo2010.cnefe_faces_gid_seq OWNED BY censo2010.cnefe_faces.gid;


--
-- TOC entry 209 (class 1259 OID 19629)
-- Name: cnefe_lotes; Type: TABLE; Schema: censo2010; Owner: -
--

CREATE TABLE censo2010.cnefe_lotes (
    gid integer NOT NULL,
    geom public.geometry(Point,4674),
    setor_id character varying(16),
    quadra smallint,
    face smallint,
    especie character varying(2),
    indicador character varying(1),
    estab_nome character varying(1000),
    lograd_tipo character varying(20),
    lograd_tit character varying(30),
    lograd_nome character varying(60),
    imovel_numero integer,
    modificador character varying(10),
    cep character varying(8),
    unidades smallint,
    andares smallint,
    aptos_andar smallint,
    testada double precision,
    posicao smallint
);


--
-- TOC entry 208 (class 1259 OID 19627)
-- Name: cnefe_lotes_gid_seq; Type: SEQUENCE; Schema: censo2010; Owner: -
--

CREATE SEQUENCE censo2010.cnefe_lotes_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3618 (class 0 OID 0)
-- Dependencies: 208
-- Name: cnefe_lotes_gid_seq; Type: SEQUENCE OWNED BY; Schema: censo2010; Owner: -
--

ALTER SEQUENCE censo2010.cnefe_lotes_gid_seq OWNED BY censo2010.cnefe_lotes.gid;


--
-- TOC entry 204 (class 1259 OID 19527)
-- Name: cnefe_quadras; Type: TABLE; Schema: censo2010; Owner: -
--

CREATE TABLE censo2010.cnefe_quadras (
    gid integer NOT NULL,
    geom public.geometry(Polygon,4674),
    codigo character varying(20),
    setor character varying(16),
    numero smallint
);


--
-- TOC entry 205 (class 1259 OID 19533)
-- Name: cnefe_quadras_gid_seq; Type: SEQUENCE; Schema: censo2010; Owner: -
--

CREATE SEQUENCE censo2010.cnefe_quadras_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3619 (class 0 OID 0)
-- Dependencies: 205
-- Name: cnefe_quadras_gid_seq; Type: SEQUENCE OWNED BY; Schema: censo2010; Owner: -
--

ALTER SEQUENCE censo2010.cnefe_quadras_gid_seq OWNED BY censo2010.cnefe_quadras.gid;


--
-- TOC entry 206 (class 1259 OID 19535)
-- Name: cnefe_setores; Type: TABLE; Schema: censo2010; Owner: -
--

CREATE TABLE censo2010.cnefe_setores (
    gid integer NOT NULL,
    geom public.geometry(Polygon,4674),
    id integer,
    geocod character varying(24),
    tipo character varying(10),
    geocodb character varying(16),
    bairro character varying(60),
    geocodd character varying(12),
    distrito character varying(60),
    geocods character varying(10),
    subdistrito character varying(60),
    geocodm character varying(7),
    municipio character varying(60),
    mesoregiao character varying(60),
    microregiao character varying(60)
);


--
-- TOC entry 207 (class 1259 OID 19541)
-- Name: cnefe_setores_gid_seq; Type: SEQUENCE; Schema: censo2010; Owner: -
--

CREATE SEQUENCE censo2010.cnefe_setores_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3620 (class 0 OID 0)
-- Dependencies: 207
-- Name: cnefe_setores_gid_seq; Type: SEQUENCE OWNED BY; Schema: censo2010; Owner: -
--

ALTER SEQUENCE censo2010.cnefe_setores_gid_seq OWNED BY censo2010.cnefe_setores.gid;


--
-- TOC entry 213 (class 1259 OID 19951)
-- Name: distritos; Type: TABLE; Schema: censo2010; Owner: -
--

CREATE TABLE censo2010.distritos (
    gid integer NOT NULL,
    geom public.geometry(Polygon,4674),
    cd_geocodd character varying(20),
    nm_distrit character varying(60)
);


--
-- TOC entry 212 (class 1259 OID 19949)
-- Name: distritos_gid_seq; Type: SEQUENCE; Schema: censo2010; Owner: -
--

CREATE SEQUENCE censo2010.distritos_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3621 (class 0 OID 0)
-- Dependencies: 212
-- Name: distritos_gid_seq; Type: SEQUENCE OWNED BY; Schema: censo2010; Owner: -
--

ALTER SEQUENCE censo2010.distritos_gid_seq OWNED BY censo2010.distritos.gid;


--
-- TOC entry 215 (class 1259 OID 19964)
-- Name: municipios; Type: TABLE; Schema: censo2010; Owner: -
--

CREATE TABLE censo2010.municipios (
    gid integer NOT NULL,
    geom public.geometry(Polygon,4674),
    cd_geocodm character varying(20),
    nm_municip character varying(60)
);


--
-- TOC entry 214 (class 1259 OID 19962)
-- Name: municipios_gid_seq; Type: SEQUENCE; Schema: censo2010; Owner: -
--

CREATE SEQUENCE censo2010.municipios_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3622 (class 0 OID 0)
-- Dependencies: 214
-- Name: municipios_gid_seq; Type: SEQUENCE OWNED BY; Schema: censo2010; Owner: -
--

ALTER SEQUENCE censo2010.municipios_gid_seq OWNED BY censo2010.municipios.gid;


--
-- TOC entry 3469 (class 2604 OID 19647)
-- Name: cnefe_enderecos id; Type: DEFAULT; Schema: censo2010; Owner: -
--

ALTER TABLE ONLY censo2010.cnefe_enderecos ALTER COLUMN id SET DEFAULT nextval('censo2010.cnefe_enderecos_id_seq'::regclass);


--
-- TOC entry 3465 (class 2604 OID 19544)
-- Name: cnefe_faces gid; Type: DEFAULT; Schema: censo2010; Owner: -
--

ALTER TABLE ONLY censo2010.cnefe_faces ALTER COLUMN gid SET DEFAULT nextval('censo2010.cnefe_faces_gid_seq'::regclass);


--
-- TOC entry 3468 (class 2604 OID 19632)
-- Name: cnefe_lotes gid; Type: DEFAULT; Schema: censo2010; Owner: -
--

ALTER TABLE ONLY censo2010.cnefe_lotes ALTER COLUMN gid SET DEFAULT nextval('censo2010.cnefe_lotes_gid_seq'::regclass);


--
-- TOC entry 3466 (class 2604 OID 19546)
-- Name: cnefe_quadras gid; Type: DEFAULT; Schema: censo2010; Owner: -
--

ALTER TABLE ONLY censo2010.cnefe_quadras ALTER COLUMN gid SET DEFAULT nextval('censo2010.cnefe_quadras_gid_seq'::regclass);


--
-- TOC entry 3467 (class 2604 OID 19547)
-- Name: cnefe_setores gid; Type: DEFAULT; Schema: censo2010; Owner: -
--

ALTER TABLE ONLY censo2010.cnefe_setores ALTER COLUMN gid SET DEFAULT nextval('censo2010.cnefe_setores_gid_seq'::regclass);


--
-- TOC entry 3470 (class 2604 OID 19954)
-- Name: distritos gid; Type: DEFAULT; Schema: censo2010; Owner: -
--

ALTER TABLE ONLY censo2010.distritos ALTER COLUMN gid SET DEFAULT nextval('censo2010.distritos_gid_seq'::regclass);


--
-- TOC entry 3471 (class 2604 OID 19967)
-- Name: municipios gid; Type: DEFAULT; Schema: censo2010; Owner: -
--

ALTER TABLE ONLY censo2010.municipios ALTER COLUMN gid SET DEFAULT nextval('censo2010.municipios_gid_seq'::regclass);


--
-- TOC entry 3478 (class 2606 OID 19959)
-- Name: distritos distritos_pkey; Type: CONSTRAINT; Schema: censo2010; Owner: -
--

ALTER TABLE ONLY censo2010.distritos
    ADD CONSTRAINT distritos_pkey PRIMARY KEY (gid);


--
-- TOC entry 3484 (class 2606 OID 19972)
-- Name: municipios municipios_pkey; Type: CONSTRAINT; Schema: censo2010; Owner: -
--

ALTER TABLE ONLY censo2010.municipios
    ADD CONSTRAINT municipios_pkey PRIMARY KEY (gid);


--
-- TOC entry 3475 (class 1259 OID 19651)
-- Name: cnefe_enderecos_id_idx; Type: INDEX; Schema: censo2010; Owner: -
--

CREATE UNIQUE INDEX cnefe_enderecos_id_idx ON censo2010.cnefe_enderecos USING btree (id);


--
-- TOC entry 3476 (class 1259 OID 19652)
-- Name: cnefe_enderecos_setor_id_idx; Type: INDEX; Schema: censo2010; Owner: -
--

CREATE INDEX cnefe_enderecos_setor_id_idx ON censo2010.cnefe_enderecos USING btree (setor_id, quadra_num, face_num);


--
-- TOC entry 3479 (class 1259 OID 19961)
-- Name: idx_distritos_geom; Type: INDEX; Schema: censo2010; Owner: -
--

CREATE INDEX idx_distritos_geom ON censo2010.distritos USING gist (geom);


--
-- TOC entry 3480 (class 1259 OID 19960)
-- Name: idx_distritos_gid; Type: INDEX; Schema: censo2010; Owner: -
--

CREATE UNIQUE INDEX idx_distritos_gid ON censo2010.distritos USING btree (gid);


--
-- TOC entry 3481 (class 1259 OID 19974)
-- Name: idx_municipios_geom; Type: INDEX; Schema: censo2010; Owner: -
--

CREATE INDEX idx_municipios_geom ON censo2010.municipios USING gist (geom);


--
-- TOC entry 3482 (class 1259 OID 19973)
-- Name: idx_municipios_gid; Type: INDEX; Schema: censo2010; Owner: -
--

CREATE UNIQUE INDEX idx_municipios_gid ON censo2010.municipios USING btree (gid);


--
-- TOC entry 3472 (class 1259 OID 19637)
-- Name: lotes_gid_idx; Type: INDEX; Schema: censo2010; Owner: -
--

CREATE UNIQUE INDEX lotes_gid_idx ON censo2010.cnefe_lotes USING btree (gid);


--
-- TOC entry 3473 (class 1259 OID 19638)
-- Name: lotes_lograd_nome_idx; Type: INDEX; Schema: censo2010; Owner: -
--

CREATE INDEX lotes_lograd_nome_idx ON censo2010.cnefe_lotes USING btree (lograd_nome);


--
-- TOC entry 3474 (class 1259 OID 19639)
-- Name: lotes_setor_id_idx; Type: INDEX; Schema: censo2010; Owner: -
--

CREATE INDEX lotes_setor_id_idx ON censo2010.cnefe_lotes USING btree (setor_id);


--
-- TOC entry 3485 (class 2620 OID 19653)
-- Name: cnefe_enderecos tgr_create_ordem; Type: TRIGGER; Schema: censo2010; Owner: -
--

CREATE TRIGGER tgr_create_ordem AFTER INSERT ON censo2010.cnefe_enderecos FOR EACH ROW EXECUTE PROCEDURE censo2010.cnefe_enderecos_create_ordem();


--
-- TOC entry 3486 (class 2620 OID 19654)
-- Name: cnefe_enderecos tgr_update_ordem; Type: TRIGGER; Schema: censo2010; Owner: -
--

CREATE TRIGGER tgr_update_ordem AFTER UPDATE ON censo2010.cnefe_enderecos FOR EACH ROW WHEN ((old.ordem <> new.ordem)) EXECUTE PROCEDURE censo2010.update_ordem();


-- Completed on 2018-08-10 21:18:55 -03

--
-- PostgreSQL database dump complete
--


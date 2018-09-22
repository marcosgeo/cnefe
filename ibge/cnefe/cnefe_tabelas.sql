--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.6
-- Dumped by pg_dump version 9.6.6

-- Started on 2017-12-11 16:01:38 -02

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 17893)
-- Name: zap; Type: SCHEMA; Schema: -; Owner: -
--

DROP SCHEMA IF EXISTS censo2010;
CREATE SCHEMA censo2010;


SET search_path = censo2010, public, pg_catalog;

--
-- TOC entry 1408 (class 1255 OID 17903)
-- Name: cnefe_enderecos_create_ordem(); Type: FUNCTION; Schema: zap; Owner: -
--

CREATE FUNCTION cnefe_enderecos_create_ordem() RETURNS trigger
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
-- TOC entry 1407 (class 1255 OID 17904)
-- Name: update_ordem(); Type: FUNCTION; Schema: zap; Owner: -
--

CREATE FUNCTION update_ordem() RETURNS trigger
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


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 204 (class 1259 OID 17896)
-- Name: cnefe_enderecos; Type: TABLE; Schema: zap; Owner: -
--

CREATE TABLE cnefe_enderecos (
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
    end_especie character varying(2),
    lograd_tipo character varying(20),
    lograd_tit character varying(30),
    lograd_nome character varying(60),
    lograd_numero smallint,
    lograd_modnum character varying(10),
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
    estabelecimento_nome character varying(40),
    endereco_indicador character varying(1),
    domicilio_coletivo character varying(30)
);


--
-- TOC entry 203 (class 1259 OID 17894)
-- Name: cnefe_enderecos_id_seq; Type: SEQUENCE; Schema: zap; Owner: -
--

CREATE SEQUENCE cnefe_enderecos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3618 (class 0 OID 0)
-- Dependencies: 203
-- Name: cnefe_enderecos_id_seq; Type: SEQUENCE OWNED BY; Schema: zap; Owner: -
--

ALTER SEQUENCE cnefe_enderecos_id_seq OWNED BY cnefe_enderecos.id;


--
-- TOC entry 206 (class 1259 OID 17950)
-- Name: cnefe_faces; Type: TABLE; Schema: zap; Owner: -
--

CREATE TABLE cnefe_faces (
    gid integer NOT NULL,
    geom geometry(LineString,4674),
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
-- TOC entry 205 (class 1259 OID 17948)
-- Name: cnefe_faces_gid_seq; Type: SEQUENCE; Schema: zap; Owner: -
--

CREATE SEQUENCE cnefe_faces_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3619 (class 0 OID 0)
-- Dependencies: 205
-- Name: cnefe_faces_gid_seq; Type: SEQUENCE OWNED BY; Schema: zap; Owner: -
--

ALTER SEQUENCE cnefe_faces_gid_seq OWNED BY cnefe_faces.gid;


--
-- TOC entry 216 (class 1259 OID 19584)
-- Name: cnefe_lotes; Type: TABLE; Schema: zap; Owner: -
--

CREATE TABLE cnefe_lotes (
    gid integer NOT NULL,
    geom geometry(Point,4674),
    setor_id character varying(16),
    quadra smallint,
    face smallint,
    especie character varying(2),
    end_indicador character varying(1),
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
    blocos character varying(30),
    posicao smallint,
    fonetica character varying(50)
);


--
-- TOC entry 215 (class 1259 OID 19582)
-- Name: cnefe_lotes_gid_seq; Type: SEQUENCE; Schema: zap; Owner: -
--

CREATE SEQUENCE cnefe_lotes_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3623 (class 0 OID 0)
-- Dependencies: 215
-- Name: cnefe_lotes_gid_seq; Type: SEQUENCE OWNED BY; Schema: zap; Owner: -
--

ALTER SEQUENCE cnefe_lotes_gid_seq OWNED BY cnefe_lotes.gid;


--
-- TOC entry 210 (class 1259 OID 18065)
-- Name: cnefe_quadras; Type: TABLE; Schema: zap; Owner: -
--

CREATE TABLE cnefe_quadras (
    gid integer NOT NULL,
    geom geometry(Polygon,4674),
    codigo character varying(20),
    setor character varying(16),
    numero smallint
);


--
-- TOC entry 209 (class 1259 OID 18063)
-- Name: cnefe_quadras_gid_seq; Type: SEQUENCE; Schema: zap; Owner: -
--

CREATE SEQUENCE cnefe_quadras_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3624 (class 0 OID 0)
-- Dependencies: 209
-- Name: cnefe_quadras_gid_seq; Type: SEQUENCE OWNED BY; Schema: zap; Owner: -
--

ALTER SEQUENCE cnefe_quadras_gid_seq OWNED BY cnefe_quadras.gid;


--
-- TOC entry 208 (class 1259 OID 18038)
-- Name: cnefe_setores; Type: TABLE; Schema: zap; Owner: -
--

CREATE TABLE cnefe_setores (
    gid integer NOT NULL,
    geom geometry(Polygon,4674),
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
-- TOC entry 207 (class 1259 OID 18036)
-- Name: cnefe_setores_gid_seq; Type: SEQUENCE; Schema: zap; Owner: -
--

CREATE SEQUENCE cnefe_setores_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3625 (class 0 OID 0)
-- Dependencies: 207
-- Name: cnefe_setores_gid_seq; Type: SEQUENCE OWNED BY; Schema: zap; Owner: -
--

ALTER SEQUENCE cnefe_setores_gid_seq OWNED BY cnefe_setores.gid;


--
-- TOC entry 3470 (class 2604 OID 17899)
-- Name: cnefe_enderecos id; Type: DEFAULT; Schema: zap; Owner: -
--

ALTER TABLE ONLY cnefe_enderecos ALTER COLUMN id SET DEFAULT nextval('cnefe_enderecos_id_seq'::regclass);


--
-- TOC entry 3471 (class 2604 OID 17953)
-- Name: cnefe_faces gid; Type: DEFAULT; Schema: zap; Owner: -
--

ALTER TABLE ONLY cnefe_faces ALTER COLUMN gid SET DEFAULT nextval('cnefe_faces_gid_seq'::regclass);


--
-- TOC entry 3476 (class 2604 OID 19587)
-- Name: cnefe_lotes gid; Type: DEFAULT; Schema: zap; Owner: -
--

ALTER TABLE ONLY cnefe_lotes ALTER COLUMN gid SET DEFAULT nextval('cnefe_lotes_gid_seq'::regclass);


--
-- TOC entry 3473 (class 2604 OID 18068)
-- Name: cnefe_quadras gid; Type: DEFAULT; Schema: zap; Owner: -
--

ALTER TABLE ONLY cnefe_quadras ALTER COLUMN gid SET DEFAULT nextval('cnefe_quadras_gid_seq'::regclass);


--
-- TOC entry 3472 (class 2604 OID 18041)
-- Name: cnefe_setores gid; Type: DEFAULT; Schema: zap; Owner: -
--

ALTER TABLE ONLY cnefe_setores ALTER COLUMN gid SET DEFAULT nextval('cnefe_setores_gid_seq'::regclass);


--
-- TOC entry 3480 (class 1259 OID 19929)
-- Name: cnefe_lotes_fonetica_idx; Type: INDEX; Schema: zap; Owner: -
--

CREATE INDEX cnefe_lotes_fonetica_idx ON cnefe_lotes USING btree (fonetica);


--
-- TOC entry 3481 (class 1259 OID 19926)
-- Name: cnefe_lotes_gid_idx; Type: INDEX; Schema: zap; Owner: -
--

CREATE UNIQUE INDEX cnefe_lotes_gid_idx ON cnefe_lotes USING btree (gid);


--
-- TOC entry 3482 (class 1259 OID 19928)
-- Name: cnefe_lotes_lograd_nome_idx; Type: INDEX; Schema: zap; Owner: -
--

CREATE INDEX cnefe_lotes_lograd_nome_idx ON cnefe_lotes USING btree (lograd_nome);


--
-- TOC entry 3483 (class 1259 OID 19927)
-- Name: cnefe_lotes_setor_id_idx; Type: INDEX; Schema: zap; Owner: -
--

CREATE INDEX cnefe_lotes_setor_id_idx ON cnefe_lotes USING btree (setor_id);


--
-- TOC entry 3478 (class 1259 OID 19694)
-- Name: zap_cnefe_enderecos_id_idx; Type: INDEX; Schema: zap; Owner: -
--

CREATE UNIQUE INDEX zap_cnefe_enderecos_id_idx ON cnefe_enderecos USING btree (id);


--
-- TOC entry 3479 (class 1259 OID 19695)
-- Name: zap_cnefe_enderecos_setor_id_idx; Type: INDEX; Schema: zap; Owner: -
--

CREATE INDEX zap_cnefe_enderecos_setor_id_idx ON cnefe_enderecos USING btree (setor_id, quadra_num, face_num);


--
-- TOC entry 3489 (class 2620 OID 17906)
-- Name: cnefe_enderecos tgr_create_ordem; Type: TRIGGER; Schema: zap; Owner: -
--

CREATE TRIGGER tgr_create_ordem AFTER INSERT ON cnefe_enderecos FOR EACH ROW EXECUTE PROCEDURE cnefe_enderecos_create_ordem();


--
-- TOC entry 3488 (class 2620 OID 17905)
-- Name: cnefe_enderecos tgr_update_ordem; Type: TRIGGER; Schema: zap; Owner: -
--

CREATE TRIGGER tgr_update_ordem AFTER UPDATE ON cnefe_enderecos FOR EACH ROW WHEN ((old.ordem <> new.ordem)) EXECUTE PROCEDURE update_ordem();


-- Completed on 2017-12-11 16:01:43 -02

--
-- PostgreSQL database dump complete
--

INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) values ( 97218, 'sr-org', 7218, '+proj=aea +lat_1=-2 +lat_2=-22 +lat_0=-12 +lon_0=-54 +x_0=0 +y_0=0 +ellps=aust_SA +units=m +no_defs ', 'PROJCS["South_America_Albers_Equal_Area_Conic",GEOGCS["GCS_South_American_1969",DATUM["South_American_Datum_1969",SPHEROID["GRS_1967_Truncated",6378160.0,298.25]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["longitude_of_center",-54.0],PARAMETER["Standard_Parallel_1",-2.0],PARAMETER["Standard_Parallel_2",-22.0],PARAMETER["latitude_of_center",-12.0],UNIT["Meter",1.0]]');
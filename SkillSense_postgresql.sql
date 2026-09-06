--
-- PostgreSQL database dump
--

\restrict 9JJEhHD8cLzg57I8uQktfkMba33KczMzcFBNkZr6pqe5eLW7dg3WLeN06SqHbiV

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-09-06 12:00:52

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 226 (class 1259 OID 16417)
-- Name: assessments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assessments (
    assessment_id integer NOT NULL,
    official_id integer,
    assessment_name character varying(100),
    assessment_date date,
    score numeric(5,2)
);


ALTER TABLE public.assessments OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16416)
-- Name: assessments_assessment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.assessments ALTER COLUMN assessment_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.assessments_assessment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 224 (class 1259 OID 16409)
-- Name: competencies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competencies (
    competency_id integer NOT NULL,
    competency_name character varying(100) NOT NULL,
    description character varying(255),
    level character varying(50)
);


ALTER TABLE public.competencies OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16408)
-- Name: competencies_competency_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.competencies ALTER COLUMN competency_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.competencies_competency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 232 (class 1259 OID 16441)
-- Name: competency_passport; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.competency_passport (
    passport_id integer NOT NULL,
    official_id integer,
    competency_id integer,
    competency_score numeric(5,2),
    competency_level character varying(50)
);


ALTER TABLE public.competency_passport OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16440)
-- Name: competency_passport_passport_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.competency_passport ALTER COLUMN passport_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.competency_passport_passport_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 220 (class 1259 OID 16386)
-- Name: departments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departments (
    department_id integer NOT NULL,
    department_name character varying(100) NOT NULL,
    description character varying(255)
);


ALTER TABLE public.departments OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16385)
-- Name: departments_department_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.departments ALTER COLUMN department_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.departments_department_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 222 (class 1259 OID 16399)
-- Name: officials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.officials (
    official_id integer NOT NULL,
    name character varying(100) NOT NULL,
    department character varying(100),
    designation character varying(100),
    role character varying(100),
    experience_years integer,
    education character varying(150),
    department_id integer
);


ALTER TABLE public.officials OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16398)
-- Name: officials_official_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.officials ALTER COLUMN official_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.officials_official_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 228 (class 1259 OID 16424)
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    question_id integer NOT NULL,
    competency_id integer,
    question_text character varying(500),
    correct_answer character varying(255),
    difficulty character varying(50)
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16423)
-- Name: questions_question_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.questions ALTER COLUMN question_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.questions_question_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 230 (class 1259 OID 16433)
-- Name: responses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.responses (
    response_id integer NOT NULL,
    assessment_id integer,
    question_id integer,
    answer_given character varying(255),
    is_correct boolean
);


ALTER TABLE public.responses OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16432)
-- Name: responses_response_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.responses ALTER COLUMN response_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.responses_response_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 5063 (class 0 OID 16417)
-- Dependencies: 226
-- Data for Name: assessments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assessments (assessment_id, official_id, assessment_name, assessment_date, score) FROM stdin;
1	1	financial skills assessment	2026-09-01	82.50
2	2	hr skills assessment	2026-09-01	76.00
3	3	public health assessment	2026-09-01	91.00
4	4	cybersecurity assessment	2026-09-02	68.50
5	5	operations assessment	2026-09-02	79.00
6	6	legal compliance assessment	2026-09-02	85.50
7	7	communication assessment	2026-09-02	73.00
\.


--
-- TOC entry 5061 (class 0 OID 16409)
-- Dependencies: 224
-- Data for Name: competencies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.competencies (competency_id, competency_name, description, level) FROM stdin;
1	financial analysis	understanding financial data and making informed decisions	advanced
2	talent management	managing employees, recruitment and development	advanced
3	public health management	managing healthcare programs and compliance	advanced
4	cybersecurity	protecting systems, data and digital infrastructure	advanced
5	operations management	managing supply chains and operational processes	intermediate
6	legal compliance	understanding laws, regulations and compliance requirements	intermediate
7	communication management	managing media, communication and public relations	advanced
\.


--
-- TOC entry 5069 (class 0 OID 16441)
-- Dependencies: 232
-- Data for Name: competency_passport; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.competency_passport (passport_id, official_id, competency_id, competency_score, competency_level) FROM stdin;
1	1	1	82.50	advanced
2	2	2	76.00	intermediate
3	3	3	91.00	advanced
4	4	4	68.50	intermediate
5	5	5	79.00	intermediate
6	6	6	85.50	advanced
7	7	7	73.00	intermediate
\.


--
-- TOC entry 5057 (class 0 OID 16386)
-- Dependencies: 220
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departments (department_id, department_name, description) FROM stdin;
1	Finance	Financial planning and management
2	Human Resources	Employee management and talent development
3	Public Health	Healthcare and public health administration
4	Information Technology	Technology, systems and cybersecurity
5	Operations	Supply chain and operational management
6	Legal Affairs	Legal compliance and regulatory matters
7	Public Relations	Communication, media and public relations
\.


--
-- TOC entry 5059 (class 0 OID 16399)
-- Dependencies: 222
-- Data for Name: officials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.officials (official_id, name, department, designation, role, experience_years, education, department_id) FROM stdin;
1	Arjun Mehta	Finance	Chief Financial Officer	Strategic financial planning and risk management	15	MBA in Finance - IIM Ahmedabad	1
2	Priya Sharma	Human Resources	HR Director	Talent acquisition, employee relations, and policy framing	12	Master of Human Resource Management	2
3	Dr. Rajesh Kumar	Public Health	Chief Medical Officer	Overseeing healthcare initiatives and clinical compliance	18	MD in Community Medicine	3
4	Sneha Kulkarni	Information Technology	Chief Information Security Officer	Managing enterprise cybersecurity and cloud infrastructure	10	B.Tech in Computer Science, CISSP Certified	4
5	Vikram Singh	Operations	Operations Manager	Supply chain optimization and logistics oversight	8	B.Tech + MBA in Operations	5
6	Ananya Das	Legal Affairs	Legal Counsel	Contract drafting, regulatory compliance, and dispute resolution	6	LL.M. (Master of Laws)	6
7	Amit Verma	Public Relations	Communications Director	Media relations, crisis communication, and brand management	14	Master in Mass Communication	7
\.


--
-- TOC entry 5065 (class 0 OID 16424)
-- Dependencies: 228
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (question_id, competency_id, question_text, correct_answer, difficulty) FROM stdin;
1	1	what is the main purpose of financial risk management?	to identify and reduce financial risks	medium
2	2	what is an important part of talent management?	employee development	medium
3	3	what is the main goal of public health management?	protecting and improving population health	medium
4	4	what is a strong way to protect an organization from cyber threats?	regular security monitoring	hard
5	5	what is a key objective of supply chain management?	efficient movement of goods and resources	medium
6	6	what is the purpose of regulatory compliance?	to ensure laws and regulations are followed	medium
7	7	what is an important part of public relations?	effective communication with the public	easy
\.


--
-- TOC entry 5067 (class 0 OID 16433)
-- Dependencies: 230
-- Data for Name: responses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.responses (response_id, assessment_id, question_id, answer_given, is_correct) FROM stdin;
1	1	1	to identify and reduce financial risks	t
2	2	2	employee development	t
3	3	3	protecting and improving population health	t
4	4	4	strong passwords	f
5	5	5	efficient movement of goods and resources	t
6	6	6	to ensure laws and regulations are followed	t
7	7	7	social media	f
\.


--
-- TOC entry 5075 (class 0 OID 0)
-- Dependencies: 225
-- Name: assessments_assessment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assessments_assessment_id_seq', 7, true);


--
-- TOC entry 5076 (class 0 OID 0)
-- Dependencies: 223
-- Name: competencies_competency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.competencies_competency_id_seq', 7, true);


--
-- TOC entry 5077 (class 0 OID 0)
-- Dependencies: 231
-- Name: competency_passport_passport_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.competency_passport_passport_id_seq', 7, true);


--
-- TOC entry 5078 (class 0 OID 0)
-- Dependencies: 219
-- Name: departments_department_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.departments_department_id_seq', 7, true);


--
-- TOC entry 5079 (class 0 OID 0)
-- Dependencies: 221
-- Name: officials_official_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.officials_official_id_seq', 7, true);


--
-- TOC entry 5080 (class 0 OID 0)
-- Dependencies: 227
-- Name: questions_question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questions_question_id_seq', 7, true);


--
-- TOC entry 5081 (class 0 OID 0)
-- Dependencies: 229
-- Name: responses_response_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.responses_response_id_seq', 7, true);


--
-- TOC entry 4895 (class 2606 OID 16422)
-- Name: assessments assessments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assessments
    ADD CONSTRAINT assessments_pkey PRIMARY KEY (assessment_id);


--
-- TOC entry 4893 (class 2606 OID 16415)
-- Name: competencies competencies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competencies
    ADD CONSTRAINT competencies_pkey PRIMARY KEY (competency_id);


--
-- TOC entry 4901 (class 2606 OID 16446)
-- Name: competency_passport competency_passport_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competency_passport
    ADD CONSTRAINT competency_passport_pkey PRIMARY KEY (passport_id);


--
-- TOC entry 4887 (class 2606 OID 16394)
-- Name: departments departments_department_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_department_name_key UNIQUE (department_name);


--
-- TOC entry 4889 (class 2606 OID 16392)
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (department_id);


--
-- TOC entry 4891 (class 2606 OID 16407)
-- Name: officials officials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.officials
    ADD CONSTRAINT officials_pkey PRIMARY KEY (official_id);


--
-- TOC entry 4897 (class 2606 OID 16431)
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (question_id);


--
-- TOC entry 4899 (class 2606 OID 16438)
-- Name: responses responses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responses
    ADD CONSTRAINT responses_pkey PRIMARY KEY (response_id);


--
-- TOC entry 4903 (class 2606 OID 16452)
-- Name: assessments fk_assessment_official; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assessments
    ADD CONSTRAINT fk_assessment_official FOREIGN KEY (official_id) REFERENCES public.officials(official_id);


--
-- TOC entry 4902 (class 2606 OID 16447)
-- Name: officials fk_official_department; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.officials
    ADD CONSTRAINT fk_official_department FOREIGN KEY (department_id) REFERENCES public.departments(department_id);


--
-- TOC entry 4907 (class 2606 OID 16477)
-- Name: competency_passport fk_passport_competency; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competency_passport
    ADD CONSTRAINT fk_passport_competency FOREIGN KEY (competency_id) REFERENCES public.competencies(competency_id);


--
-- TOC entry 4908 (class 2606 OID 16472)
-- Name: competency_passport fk_passport_official; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.competency_passport
    ADD CONSTRAINT fk_passport_official FOREIGN KEY (official_id) REFERENCES public.officials(official_id);


--
-- TOC entry 4904 (class 2606 OID 16457)
-- Name: questions fk_question_competency; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT fk_question_competency FOREIGN KEY (competency_id) REFERENCES public.competencies(competency_id);


--
-- TOC entry 4905 (class 2606 OID 16462)
-- Name: responses fk_response_assessment; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responses
    ADD CONSTRAINT fk_response_assessment FOREIGN KEY (assessment_id) REFERENCES public.assessments(assessment_id);


--
-- TOC entry 4906 (class 2606 OID 16467)
-- Name: responses fk_response_question; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responses
    ADD CONSTRAINT fk_response_question FOREIGN KEY (question_id) REFERENCES public.questions(question_id);


-- Completed on 2026-09-06 12:00:52

--
-- PostgreSQL database dump complete
--

\unrestrict 9JJEhHD8cLzg57I8uQktfkMba33KczMzcFBNkZr6pqe5eLW7dg3WLeN06SqHbiV


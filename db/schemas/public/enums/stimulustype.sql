--
-- Name: stimulustype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.stimulustype AS ENUM (
    'image',
    'audio',
    'video',
    'html',
    'ema',
    'recording'
);


ALTER TYPE public.stimulustype OWNER TO postgres;
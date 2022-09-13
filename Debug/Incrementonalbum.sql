


ALTER TABLE public.albums ALTER COLUMN idalbum ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.albums_idalbum_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
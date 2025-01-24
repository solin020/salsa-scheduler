--
-- Name: update_users(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.update_users()
    LANGUAGE plpgsql SECURITY DEFINER
    AS $_$
BEGIN                                                                                                                  
         COPY(SELECT                                                                                                    
                    'ADMINS="'                                                                                          
                 || array_to_string((SELECT ARRAY(SELECT format('%L', id) FROM admins)),       ',')
                 || E'"\n' || 'COORDINATORS="'                                                                          
                 || array_to_string((SELECT ARRAY(SELECT format('%L', id) FROM coordinators)), ',')
                 || E'"\n' || 'ANNOTATORS="'                                                                            
                 || array_to_string((SELECT ARRAY(SELECT format('%L', id) FROM annotators)),   ',')
                 || E'"\n'                                                                                              
         ) TO PROGRAM $inner$perl -pe 's/\\n/\n/g'> /access-control/roles.txt$inner$;                                   
 END;
$_$;


ALTER PROCEDURE public.update_users() OWNER TO postgres;

--
-- Name: PROCEDURE update_users(); Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON PROCEDURE public.update_users() FROM PUBLIC;
GRANT ALL ON PROCEDURE public.update_users() TO salsa;
GRANT ALL ON PROCEDURE public.update_users() TO admin;
GRANT ALL ON PROCEDURE public.update_users() TO coordinator;

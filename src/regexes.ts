export function id_regex_test(s:string){
    return /^[a-z1-9_][a-z1-9_.@-]+$/.test(s) || 
    `Identifiers must consist entirely of lowercase letters, underscores, dashes, @signs, or periods, 
    and must start with a letter, number, or underscore`
}
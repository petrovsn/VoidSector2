


export function long_machingen_viewer(s){
    if (!s) return ""
    let slen = s.length
    if (slen<=12) return s
    return s.substr(0,4)+"..."+s.substr(slen-4,4)
}

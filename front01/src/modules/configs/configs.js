
const server_ip = "localhost"
export const server_url_ws =  "ws://" +server_ip+":5000/"
export const server_url_http = "http://"+server_ip+":1924/"
//export const ip = "192.168.1.4"


export function is_local(){
 //return false
 return server_ip==="localhost"
}





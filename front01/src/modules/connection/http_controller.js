
import { server_url_http } from "../configs/configs";
import { data_storage } from "../support/shared_storage";

export function http_request(endpoint, method, header, body, onSuccess, onFailure){
    let url = server_url_http+endpoint

    var myInit = {
        method: method,
        headers: Object.assign({
          "authToken":data_storage.get_data("AuthController.auth_token")
        },header)
      }
      if (Object.keys(body).length > 0 ){
        myInit["body"] = JSON.stringify(body)
      }

    
      console.log("request.address", url, myInit)
      let message_code = null
      return fetch(url, myInit)
        .then(response => {
          message_code = response.status;
          console.log("request.code", message_code)
          return response
        })
        .then((response)=>{
            if (message_code===200){
                return response.json()
            }
            return null
        })
        .then((data) => {
          if (message_code===200){
            console.log("request.proceed", url, myInit, data)
            if (onSuccess ) onSuccess (data)
          }
          else{
            if (onFailure) onFailure(message_code)
          }

    
        })
        .catch(
          (e) => {
            console.log("request.error", endpoint, myInit, e)

            
          }
        )
}

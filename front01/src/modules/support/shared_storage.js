



class DataStorage {
    constructor() {
        this.data_storage = {
            "Radar.scale":0,
        }
        this.onSubscribed = {

        }
    }

    print = () =>{
        console.log("DataStorage", this.data_storage, this.onSubscribed)
    }

    save_data = (key, data) => {
        if (!(key in this.data_storage)) {
            this.data_storage[key] = null
        }
        this.data_storage[key] = data
        this.execute_subscribed(key)
    }

    //ключ - событие, funcname - идентификатор подмены объекта, 
    //чтобы не плодить лишние фунции на переходах страниц, func - сам объект функции
    //чаще всего используется как эрзац замена redux чтобы не грузить проц постоянным
    //рефрешем страниц
    onSubscribe = (key, func_name, func) =>{
        if (!(key in this.onSubscribed)) {
            this.onSubscribed[key] = {}
        }
        this.onSubscribed[key][func_name] = func
    }

    execute_subscribed = (key) =>{
        for(let funcname in this.onSubscribed[key]){
            this.onSubscribed[key][funcname]()
        }
    }

    get_data = (key, pathtovalue) => {
        if (!(key in this.data_storage)) {
            return null
        }
        if (!pathtovalue) return this.data_storage[key]
        let tmp = Object.assign({}, this.data_storage[key])
        let subkeys = pathtovalue.split('.')
        for (let i in subkeys) {
            tmp = tmp[subkeys[i]]
        }
        return tmp
    }
}

export const data_storage = new DataStorage()

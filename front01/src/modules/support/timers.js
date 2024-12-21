class UpdateTickTimerCounter {
    constructor() {
        this.timers = {}
    }
    add = (key, timer) => {
        this.timers[key] = timer
    }
    get = (key) => {
        return this.timers[key]
    }

    create_new = (timer_name, func, period_ms) =>{
        let timer_id = this.get(timer_name)
        if (!timer_id) {
            clearInterval(timer_id)
        }
        timer_id = setInterval(func, period_ms)
        this.add(timer_name, timer_id)
    }

    delete = (timer_name) =>{
        let timer_id = this.get(timer_name)
        if (!timer_id) {
            clearInterval(timer_id)
        }
    }
}


export let timerscounter = new UpdateTickTimerCounter()

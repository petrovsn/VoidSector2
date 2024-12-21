import React from 'react'
import { timerscounter } from '../../support/timers';
export class PressableButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            "pressed":false
        }
    }

    componentDidMount(){
        timerscounter.create_new(this.constructor.name+this.props.label, (e)=>{
            this.proceed_tick()
        }, 50)
    }
    componentWillUnmount(){
        timerscounter.delete(this.constructor.name+this.props.label)
    }

    proceed_tick = () =>{
        if (this.state.pressed){
            this.props.onPress()
        }
    }

    press_btn = () =>{
        this.setState({"pressed":true})
    }

    uppress_btn = () =>{
        this.setState({"pressed":false})
        if (this.props.onUnpress){
            this.props.onUnpress()
        }
    }

    render(){
        return(<button 
            onMouseDown={this.press_btn} 
            onMouseUp={this.uppress_btn} 
            onMouseLeave={this.uppress_btn}>{this.props.label}</button>)
    }
}

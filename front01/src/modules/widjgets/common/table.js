import React from 'react'
import { get_locale } from '../../locales/locales'
import { long_machingen_viewer } from '../support/viewers'

import '../../styles/Table.css'

export class Table extends React.Component {
    get_header = () =>{
        let header = [<th>{get_locale("idx")}</th>]

        
        for (let i in this.props.keys) {
          header.push(<th>{get_locale(this.props.keys[i])}</th>)
        }
        return (<thead><tr>{header}</tr></thead>)
    }

    get_body = () =>{
        let body = []
        for (let row_idx in this.props.content){
            let row = [<td>{long_machingen_viewer(row_idx)}</td>]
            for (let j in this.props.keys){
                let key_name = this.props.keys[j]
                let value = ""
                if (key_name in this.props.content[row_idx])
                    if ((this.props.cell_viewers)&&(key_name in this.props.cell_viewers)){
                        value = this.props.cell_viewers[key_name](this.props.content[row_idx][key_name])
                    }
                    else {
                        value = get_locale(String(this.props.content[row_idx][key_name]))
                    }
                row.push(<td>{value}</td>)
            }
            body.push(<tr>{row}</tr>)
        }
        return (<tbody>{body}</tbody>)
    }

    render() {
        return <table>
            {this.get_header()}
            {this.get_body()}
        </table>

       
    }
}

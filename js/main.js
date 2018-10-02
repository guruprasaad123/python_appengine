
import React,{Component} from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import SearchList from './SearchList';
import {
    TextField,
    Button,
  } from '@material-ui/core'


class App extends Component
{
constructor(props)
{
    super(props);
    this.state={
        'search':'platform'
    };
    this.handleChange=this.handleChange.bind(this);
    this.handleSubmit=this.handleSubmit.bind(this);
}

handleChange(e)
{
    this.setState({
        'search':e.target.value
    });
console.log('value =>',e.target.value);
}

handleSubmit(e)
{
    const {search} = this.state;
axios.post('/search',{
    'search':search
}).then( (Response)=>{
    console.log('response : ',Response);

    this.setState({
        'results':Response.data
    })
} ).catch( (Error) =>{
    console.log('Error : ',Error.message);
})
}
render(){
const {results} = this.state;

return (

    <div style={{
margin:"0px"
    }}>
    <form
    method={'post'}
    className={'form'}
    style={{
     'padding':'10px',
     'margin':'10px'
    }}>
        <TextField
          id="name"
          label="Name"
          className={'textfield'}
          value={this.state.search}
          onChange={this.handleChange}
          margin="normal"
        />
        <Button
        variant="outlined"
         style={{
             'margin':'10px'
         }}
         onClick={this.handleSubmit}
         >
        SEARCH
        </Button>
        </form>

{results && <SearchList
             listData={results.data}
             listNumber={results.number}
/>}

        </div>

)
}



}

ReactDOM.render(<App/>,document.getElementById('app'));

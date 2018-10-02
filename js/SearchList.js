import React,{Component} from 'react';
import { withStyles } from '@material-ui/core/styles';
import {
    List ,
    ListSubheader ,
    ListItem ,
    ListItemText
    } from '@material-ui/core';

const styles = theme => ({
    root: {
      width: '100%',
      maxWidth: 360,
      backgroundColor: theme.palette.background.paper,
      position: 'relative',
      overflow: 'auto',
      maxHeight: 300,
    },
    listSection: {
      backgroundColor: 'inherit',
    },
    ul: {
      backgroundColor: 'inherit',
      padding: 0,
    },
  });

  class SearchList extends Component{


    constructor(props){
     super(props);
    }

    render(){
  const { classes,listData,listNumber } = this.props;

  return (
    <List className={classes.root} subheader={<li />}>
      {listData.map( ( listObject,indexId )=> (
        <li key={`section-${indexId}`} className={classes.listSection}>
          <ul className={classes.ul}>
            <ListSubheader>{`Title : ${listObject.title}`}</ListSubheader>
            {Object.entries(listObject).map(item => (
              <ListItem key={`item-${indexId}`}>
                <ListItemText primary={`<b> ${item[0]} </b> : ${item[1]}`} />
              </ListItem>
            ))}
          </ul>
        </li>
      ))}
    </List>
  );
}

  }


export default withStyles(styles)(SearchList);

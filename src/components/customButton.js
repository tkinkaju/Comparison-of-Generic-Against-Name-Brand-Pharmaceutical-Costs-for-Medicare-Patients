import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import { updateMap } from '../app';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  }
}));
//
export default function ContainedButtons({props}) {
  const classes = useStyles();
 
  const handleClick = () =>{
    updateMap(props)
  }
  
  return (
    <div className={classes.root}>
      <Button variant="contained" color='primary' onClick={handleClick}>Search</Button>
    </div>
  );
}

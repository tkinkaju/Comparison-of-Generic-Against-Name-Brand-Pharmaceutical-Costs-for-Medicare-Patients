import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import { updateDrug } from '../app';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

export default function SimpleSelect() {
  const classes = useStyles();
  const [age, setAge] = React.useState('');
  var dropDownValue = "Drug"
  const handleChange = (event) => {
    updateDrug(event.target.value);
    dropDownValue = event.target.value
  };

  return (
    <div>
      <FormControl className={classes.formControl}>
        <InputLabel id="demo-simple-select-label" >{dropDownValue}</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={age}
          onChange={handleChange}
          fullWidth={true}
        >
          <MenuItem value={"Adalimumab"}>Adalimumab</MenuItem>
          <MenuItem value={"Atorvastatin Calcium"}>Astorvastatin Calcium</MenuItem>
          <MenuItem value={"Donepezil Hcl"}>Donepezil Hcl</MenuItem>
          <MenuItem value={"Etanercept"}>Etanercept</MenuItem>
          <MenuItem value={"Sertraline Hcl"}>Sertraline Hcl</MenuItem>
          <MenuItem value={"Vortioxetine Hydrobromide"}>Vortioxetine Hydrobromide</MenuItem>
          <MenuItem value={"Zolpidem Tartrate"}>Zolpidem Tartrate</MenuItem>
        </Select>
      </FormControl>
      </div>
  )
}

spans = document.querySelectorAll('span');
for (var j = 0; j < spans.length; j++) {
    spans[j].classList.add('d-block');
}


labels = document.querySelectorAll('label');

for (var i = 0; i < labels.length; i++) {
    labels[i].classList.add('form-label');
}

inputs = document.querySelectorAll('input');
for (var i = 0; i < inputs.length; i++) {
    inputs[i].classList.add('form-control');
}
select= document.querySelector('select')

select.classList.add('form-control')

divs = document.getElementsByClassName("form_element")
for (var d =0; d < divs.length; d++){
    divs[d].classList.add('mb-3')
}

checkboxex=document.querySelectorAll('input[type="checkbox"]')
for (var d =0; d < checkboxex.length; d++){
    checkboxex[d].classList.remove('form-control')
}

errors = document.getElementsByClassName('errorlist')
for (var m=0 ; m < errors.length; m ++){
    divs[m].style = 'color:red; font-weight: bold';
}
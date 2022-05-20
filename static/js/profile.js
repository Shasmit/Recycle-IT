
const imgDiv = document.querySelector('.profilepic');
const img = document.querySelector('#photo');
const file = document.querySelector('#file');
const uploadBtn = document.querySelector('#uploadBtn');
const form = document.querySelector('.profilepic form');


//hoper profile

imgDiv.addEventListener('mouseenter', function()
{
    uploadBtn.style.display = "block"
});

imgDiv.addEventListener('mouseleave', function()
{
    uploadBtn.style.display='none';
});

file.addEventListener('change', function(event)
{
    const chooseFile = this.files[0];

    if (chooseFile){
        const reader = new FileReader();

        // form.submit()
        reader.addEventListener('load', function(){
            img.setAttribute('src', reader.result);
        });

        reader.readAsDataURL(chooseFile);

    }
});
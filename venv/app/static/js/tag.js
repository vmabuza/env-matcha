[].forEach.call(document.getElementsByClassName('tags-input'), function (el) {
    let hiddenInput = document.createElement('input'),
        mainInput = document.createElement('input'),
        tags = [];
    
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', el.getAttribute('data-name'));

    mainInput.setAttribute('type', 'text');
    mainInput.classList.add('main-input');
    mainInput.addEventListener('input', function () {
        let enteredTags = mainInput.value.split(',');
        if (enteredTags.length > 1) {
            enteredTags.forEach(function (t) {
                let filteredTag = filterTag(t);
                if (filteredTag.length > 0)
                    addTag(filteredTag);
            });
            mainInput.value = '';
        }
    });

    mainInput.addEventListener('keydown', function (e) {
        let keyCode = e.which || e.keyCode;
        if (keyCode === 8 && mainInput.value.length === 0 && tags.length > 0) {
            removeTag(tags.length - 1);
        }
    });

    mainInput.addEventListener('keydown',(e) =>{

        let keyCode = e.which || e.keyCode;
        
        if(keyCode === 13){
            let enteredTags = mainInput.value.split(',')
            enteredTags.forEach(function(e){
                let filteredTag = filterTag(e);
                if(filteredTag.length > 0)
                    addTag(filteredTag)
            });
            mainInput.value = '';
        }
    
    })

   
    el.appendChild(mainInput);
    el.appendChild(hiddenInput);

    var interest = document.getElementById('interest').innerText
            
            
            
            
    function filterT (tag) {
        return tag.replace(/\s+/g, ',');
    }

    var look = filterT(interest)
    console.log(look)

    let entered = look.split(',');

    if (entered.length > 1) {
        entered.forEach(function (t) {
            let filteredTag = filterTag(t);
            if (filteredTag.length > 0)
                addTag(filteredTag);
        })
    }
    // addTag(entered)


    function addTag (text) {
        let tag = {
            text: text,
            element: document.createElement('span'),
        };

        tag.element.classList.add('tag');
        tag.element.textContent = tag.text;

        // newlink = document.createElement('a');
        // newlink.setAttribute('class', 'signature');
        // div = document.querySelector('signature');
        // el.insertBefore(newlink,mainInput);
        // newlink.innerHTML=el.element
       

        let closeBtn = document.createElement('span');
        closeBtn.classList.add('close');
        closeBtn.addEventListener('click', function () {
            removeTag(tags.indexOf(tag));
        });
        tag.element.appendChild(closeBtn);

        tags.push(tag);

        el.insertBefore(tag.element,mainInput);

        refreshTags();
    }

  

    function removeTag (index) {
        let tag = tags[index];
        tags.splice(index, 1);
        el.removeChild(tag.element);
        refreshTags();
    }

    function refreshTags () {
        let tagsList = [];
        tags.forEach(function (t) {
            tagsList.push(t.text);
        });
        hiddenInput.value = tagsList.join(',');
    }

    function filterTag (tag) {
        
        return tag.trim();
    }
});


[].forEach.call(document.getElementsByClassName('tag'), function (el) {
    el.addEventListener('click',(e)=>{
        // console.log(e)
        var names = (e.target.innerText)
        console.log(e.target.className)

        if(names[0] === '#'){
            var new_names = names.replace(/#/,'')
            console.log(new_names)
            if(e.target.className === 'tag'){
                window.open("http://127.0.0.1:5000/hash_tag/"+new_names ,'_self');
            }

        }else if(e.target.className === 'tag'){
            window.open("http://127.0.0.1:5000/hash_tag/"+names ,'_self');
        }
        // console.log(typeof(names))

    })
})
//THIS JAVASCRIPT ONLY SAVES COMMENTS TO THE LOCAL DISK, THEY WILL PERSIST ON THE USERS MACHINE BUT NOT ON THE SERVER

function submitCom(){//saves the comment to localdisk or clears the local storage if clear is used as the comment name
    if($('#namebox').val() === "Clear"){
        clearStorage();//if Clear is typed as the comment name then this will clear the localstorage
        return;
    }
    var Comment_Header = $('#namebox').val();//Get the text typed in to name and comment and save it
    var Comment_body = $('#textbox').val();
    if(Comment_Header === ''){
        Comment_Header = 'Anonymous';//if someone doesnt type a name set it to anonymous
    }

    var comhtml = '<section>' +
        '<h4>' + escapeHtml(Comment_Header) + '</h4>' +
        '<p>' +
        escapeHtml(Comment_body) +
        '</p>' +
        '</section>';/*the html that will surround the comment text when inserted into the comment list.
        The escapehtml function prevents the user inserting javascript or html into the website*/

    if(Comment_body === ''){//check the comment contains something
    alert('Your comment must contain something')
    }else{
        if(typeof getStorage('Comments') === 'null'){
            setStorage('Comments', comhtml);
        } else {
            setStorage('Comments',
            comhtml +
            getStorage('Comments'));//prepend the comment to the localstorage
        }
        showCom();//reload the comments
    }

}

function escapeHtml(text) {//this function filters through several html and javascript special characters and replaces them with their text equivalents
    //I did not write this function i found it on stack overflow and as it was
    //presented as the fastest way to do this I didnt see a reason to write a my own function which could only be worse.
    //http://stackoverflow.com/questions/1787322/htmlspecialchars-equivalent-in-javascript
    var map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };

    return text.replace(/[&<>"']/g, function(m) { return map[m]; });//replaces any char in text that matches the regex /[&<>"']/g with its maped value
}

function showCom(){//loads in the comments
    $('#comments').html(getStorage('Comments'));

}

function clearCom(){//clears the input fields
    $('#namebox').val('');
    $('#textbox').val('');
}

//localstorage wrappers
function setStorage(key, value){
    window.localStorage.setItem(key, value);
}

function getStorage(key){
    return window.localStorage.getItem(key);
}

function clearStorage(){
        window.localStorage.clear();
        showCom();
};




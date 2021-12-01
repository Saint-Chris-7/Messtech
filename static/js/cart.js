var updateBtns = document.getElementsByClassName('add-cart')

for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        
        console.log('productId: ', productId, ' action: ', action)
        console.log("USER:", user)
        if (user=="AnonymousUser"){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })
}
function updateUserOrder(productId, action){
    console.log('user is logged in')
    var url = "/update_item/"
    fetch(url,{
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) =>{ 
        if (!response.ok) {
            // error processing
            throw 'Error';
        }
        return response.json()
    })
    .then((data) =>{
        console.log('data', data)
        location.reload()
    })
}
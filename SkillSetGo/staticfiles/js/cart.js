var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var id = this.dataset.id
        var action = this.dataset.action
        console.log('ProductID:', id, 'Action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('User is not authenticazted')
        }else{
            console.log('User authenticated, sending data')
        }
    })
}
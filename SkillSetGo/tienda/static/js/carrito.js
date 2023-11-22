var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var claseId = this.dataset.clase
        var action = this.dataset.action
        console.log('claseId:', claseId, 'Action:', action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('No esta logeado')
        }else{
            console.log('Esta logeado')
        }
    })
}

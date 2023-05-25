var updateButtons = document.getElementsByClassName('update-wishlist')

for(var i=0; i < updateButtons.length;i++){
    updateButtons[i].addEventListener('click',function(){
        var productId = this.dataset.wishlistproduct
        var action = this.dataset.wishlistaction
        console.log('productId:',productId,'action:',wishlistaction)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console,log('Not Logged In')
        }else{
            updateUserOrder(productId, action)
        }
    })
}
 
var sellExist = document.getElementsByClassName('sell-exist')
document.getElementById('hiddenForImage').value = 0
for (i = 0; i < sellExist.length; i++) {
	sellExist[i].addEventListener('click', function(){
        console.log(this.dataset.productdigi)

		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)
        
        document.getElementById('id_name').value = this.dataset.productnam
        console.log(document.getElementById('id_name') )
        // document.getElementById('id_name').style = "visibility:hidden"
        document.getElementById('id_name').style.display = "none"
        console.log(document.getElementById('id_name').value)
        document.getElementById('id_price').value = this.dataset.productprice
        document.getElementById('id_image').value = ""
        document.getElementById('hiddenForImage').value = 1

        console.log(this.dataset.productdigi)

        console.log(typeof this.dataset.productdigi)
        if (this.dataset.productdigi == "true")
        {
            document.getElementById('id_digital').value = "Yes"
        }
        else if (this.dataset.productdigi == "false")
        {
            document.getElementById('id_digital').value = "No"
        }

        document.getElementById('id_stock').value = this.dataset.productstock

        document.getElementbyId('hiddenForEvent').value = "sell"

        
	})
}

var resetBtn = document.getElementById('reset0')
resetBtn.addEventListener('click', function(){

    //document.getElementById('id_name').disabled =false
    document.getElementById('id_name').value = ""
    document.getElementById('id_price').value = ""
    document.getElementById('id_image').value = ""
    document.getElementById('id_digital').value = ""
    document.getElementById('id_stock').value = ""
    document.getElementById('hiddenForImage').value = 0
    document.getElementbyId('hiddenForEvent').value = "sell"

})

var rem = document.getElementsByClassName('remove-yourprods')

for (i = 0; i < rem.length; i++) {
    rem[i].addEventListener('click', function(){
    
    
        document.getElementById('whatProdIDtoRem').value = this.dataset.product
        document.getElementById('whatSellerProdRem').value = this.dataset.sellerid
        document.getElementById('hiddenForEvent').value = "remove";
        console.log(this.dataset.sellerid)
        document.getElementById('forRem').click()

	})
}
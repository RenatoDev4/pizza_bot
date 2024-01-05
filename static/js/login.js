document.addEventListener('DOMContentLoaded', function () {
    var registroForm = document.getElementById('registroForm');
    var registrarNovoBtn = document.getElementById('registrarNovoBtn');

    
    document.getElementById('registrarNovoBtn').addEventListener('click', function () {
        registroForm.style.display = 'block';  
    });

    
    registrarNovoBtn.addEventListener('click', function () {
        
        document.getElementById('registroName').value = document.getElementById('input').value;
        document.getElementById('registroNickname').value = document.getElementById('input').value;
        
        
        registroForm.submit();
    });
});

document.addEventListener('DOMContentLoaded', function () {
   
    var explicacaoTexto = document.getElementById('explicacaoTexto');
    
    
    var textoExplicativo = "Este aplicativo utiliza a inovadora tecnologia de Inteligência Artificial Generativa para desempenhar o papel de um assistente virtual para pedidos em uma pizzaria. \
    Assegura-se sempre uma compreensão abrangente de todas as opções, extras e tamanhos de pizzas disponíveis durante a interação, garantindo uma experiência de pedido personalizada. Adicionalmente, responde de maneira amigável e conversacional, proporcionando uma interação agradável e eficiente para o cliente. \
    Importante notar que este aplicativo não deve ser utilizado para fins comerciais, alem disso pode conter bugs."

    
    function typeWriter(text, index) {
      if (index < text.length) {
        explicacaoTexto.innerHTML += text.charAt(index);
        index++;
        setTimeout(function() {
          typeWriter(text, index);
        }, 30); 
      } else {
        
        document.getElementById('explicacao').style.opacity = 1;
      }
    }

    
    typeWriter(textoExplicativo, 0);
  });
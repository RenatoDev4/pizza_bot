document.addEventListener('DOMContentLoaded', function () {
    var registroForm = document.getElementById('registroForm');
    var registrarNovoBtn = document.getElementById('registrarNovoBtn');

    // Adicione um listener ao botão "Registrar novo usuário"
    document.getElementById('registrarNovoBtn').addEventListener('click', function () {
        registroForm.style.display = 'block';  // Exibe o formulário de registro
    });

    // Adicione um listener ao botão "Registrar" dentro do formulário
    registrarNovoBtn.addEventListener('click', function () {
        // Preencha os campos ocultos com os dados do campo de login
        document.getElementById('registroName').value = document.getElementById('input').value;
        document.getElementById('registroNickname').value = document.getElementById('input').value;
        
        // Submeta o formulário de registro
        registroForm.submit();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Selecione o elemento do texto explicativo
    var explicacaoTexto = document.getElementById('explicacaoTexto');
    
    // Texto a ser exibido com efeito de digitação simulada
    var textoExplicativo = "Este aplicativo atua como um assistente virtual no atendimento ao cliente (generativo) de uma pizzaria. \
    Adotando uma abordagem paciente, espera a conclusão do pedido antes de verificar se há algo mais a ser adicionado. Após essa etapa, encaminha para a coleta ou fornecimento de informações necessárias para o pagamento. Em casos de entrega, solicita o endereço; em retiradas, fornece os dados da loja. \
    É fundamental garantir a compreensão de todas as opções, extras e tamanhos disponíveis durante a interação, assegurando uma experiência de pedido personalizada. Além disso, responde de maneira amigável e conversacional, proporcionando uma interação agradável e eficiente para o cliente. \
    Este aplicativo não deve ser usado para fins comerciais, pode conter bugs."

    // Função para adicionar o efeito de digitação simulada
    function typeWriter(text, index) {
      if (index < text.length) {
        explicacaoTexto.innerHTML += text.charAt(index);
        index++;
        setTimeout(function() {
          typeWriter(text, index);
        }, 30); // Ajuste a velocidade da digitação aqui
      } else {
        // Exiba o formulário de login após a conclusão do efeito de digitação
        document.getElementById('explicacao').style.opacity = 1;
      }
    }

    // Inicie o efeito de digitação simulada
    typeWriter(textoExplicativo, 0);
  });
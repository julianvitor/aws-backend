# aws-backend
# Backend interview challenge
Data conversion and storage in a database using Amazon Web Services.
#The following instructions are in Portuguese. If you need them in English, please use Google Translate.

faça login na conta da AWS e acessar o console do CloudFormation.

No console, clique no botão "Create Stack" para criar uma nova stack e selecione a opção "Upload a template file" na tela "Create Stack". Em seguida, selecione o arquivo do template CloudFormation (cloundformation.yml) e clique em "Next".

Na tela "Specify stack details", forneça um nome para a stack e especifique os parâmetros necessários, o arquivo de cloundformation.yml utiliza parâmetros genericos, é necessario que sejam subsituidos por questões de segurança.

Clique em "Next" e especifique as opções de configuração adicionais, como tags e permissões de acesso. Em seguida, revise as informações da stack na tela seguinte e, se estiver tudo correto, clique em "Create stack" para iniciar a criação da stack.

Aguarde até que a stack seja criada com sucesso. O tempo necessário pode variar dependendo da complexidade do template e dos recursos a serem criados. Quando a stack estiver pronta, você poderá acessar a aplicação no endereço fornecido pelo Elastic Beanstalk 

cd /folder_cu_contract

solcjs --optimize --abi --bin -o . CarRegistry.sol
solcjs --optimize --abi --bin -o . Car.sol   


web3j generate solidity -b ./CarRegistry.bin -a ./CarRegistry.abi -o ./ -p java_class   
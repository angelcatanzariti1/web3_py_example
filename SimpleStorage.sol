//SPDX-Licence-Identifier: MIT

pragma solidity >=0.6.0;

contract SimpleStorage{

    uint256 favoriteNumber;

    struct People{
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;

    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favNumber) public returns(uint256){
        favoriteNumber = _favNumber;
        return _favNumber;
    }

    function retrieve() public view returns(uint256){
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favNumber) public{
        people.push(People(_favNumber, _name));
        nameToFavoriteNumber[_name] = _favNumber;
    }
}
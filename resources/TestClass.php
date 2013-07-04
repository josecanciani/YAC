<?php

class TestClass extends TestParentClass {

    function method1(Pepe1 $par1, $par2) {
        $par1 = new Pepe2();
        $par1->selfhola();
        Pepe::selfHola();
        return null;
    }

}

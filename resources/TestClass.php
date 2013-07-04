<?php

class TestClass extends TestParentClass {

    function method1(HintClass $par1, $par2) {
        $par1 = new NewClass();
        $par1->selfhola();
        Pepe::selfHola();
        return null;
    }

}

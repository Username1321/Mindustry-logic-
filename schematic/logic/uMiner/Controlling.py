p, a = ("quasar", "mega", "pulsar", "poly", "mono"), ""
for i in range(len(p)):
    a = a + f'''# {p[i]}
    
    #Bind unflagged unit

        return:
        ubind @{p[i]}
        sensor uFlag @unit @flag
        jump return notEqual uFlag 0
        read @counter cell {i+48}

    #initialize

        init_loop:
        ubind @{p[i]}
        sensor uiCap @unit @itemCapacity
        jump init_loop equal @unit null
        set cell cell1
        end

    #unit rally/release

        ulocate building rally false @copper bcCX bcCY bcCFound bcCenter            #buildingCommand-center
        ulocate building core false @copper bcX bcY 0 bCore         #buildingCore
        sensor uiType @unit @firstItem
        jump uStatus_rally equal uiType null

            sensor bciTotal bCore uiType            #dump item if buildingCoreItemTotal reached buildingcoreItemCapacity
            jump dump_item lessThan bciTotal bciCap

                set bCore @air

            dump_item:
            ucontrol itemDrop bCore 999 0 0
            ucontrol stop 0 0 0 0 0 0
            ucontrol approach bcX bcY 5 0 0
            end

        uStatus_rally:
        #read the location jump, check if direction goes to ulocate core or else
        read uStatus cell1 {i+48}
        jump bcC_rally notEqual uStatus 11

            ucontrol approach @thisx @thisy {12-(i*2)} 0 0          #rally range
            end

        bcC_rally:
        jump bc_rally equal bcCFound false

            jump bc_rally notEqual uStatus 9

                ucontrol approach bcCX bcCY {12-(i*2)} 0 0
                end
            
        bc_rally:
        ucontrol approach bcX bcY {12-(i*2)} 0 0
        end

    #unit mining controlling

        #count unit until reach limit
        jump uCounter_add lessThan uCounter limit

            set uCounter 0
            counter_jump:
            op add @counter counter @counter

                set iMine @titanium
                read limit cell1 {6*i}
                jump counter_add always

                set iMine @coal
                read limit cell1 {6*i+1}
                jump counter_add always

                set iMine @copper
                read limit cell1 {6*i+2}
                jump counter_add always

                set iMine @lead
                read limit cell1 {6*i+3}
                jump counter_add always

                set iMine @sand
                read limit cell1 {6*i+4}
                jump counter_add always

                set iMine @scrap
                read limit cell1 {6*i+5}
                set counter -3
                sensor bciCap bCore @itemCapacity
                op sub dTime @time lTime
                set lTime @time
                write dTime cell1 {i+42}

            counter_add:
            op add counter counter 3
            jump counter_jump lessThan limit 1

        uCounter_add:
        op add uCounter uCounter 1
        ulocate building core false 0 bcX bcY 0 bCore
        ucontrol within bcX bcY 26.5 bccDrop 0          #if unit near core, for auto drop
        jump bccDrop_false equal bccDrop false

            ulocate ore core false iMine oX oY 0 0
            ucontrol mine oX oY 0 0 0
            ucontrol itemDrop bCore 999 0 0 0
            sensor uMining @unit @mining
            jump approach_ore equal uMining true

                sensor uiType @unit @firstItem
                jump approach_ore equal uiType null

                    sensor bciTotal bCore uiType            #dump item if buildingCoreItemTotal reached buildingcoreItemCapacity
                    jump approach_bCore lessThan bciTotal bciCap

                        ucontrol itemDrop @air 999 0 0 0
                        jump mine_ore always

        bccDrop_false:
        sensor oX @unit @mineX
        jump check_item lessThan oX 0           # aswell check if unit mining

            sensor oY @unit @mineY
            jump approach_ore greaterThanEq oY 0

        check_item:
        ulocate ore core false iMine oX oY 0 0
        sensor uimTotal @unit iMine         #unitItemMineTotal
        sensor uiTotal @unit @totalItems            #unitItemTotal
        jump approach_bCore notEqual uimTotal uiTotal

            jump mine_ore lessThan uimTotal uiCap

        approach_bCore:
        ucontrol approach bcX bcY 5 0 0
        end
        
        print "Logic 5 uType uMiner made by: Username"

        mine_ore:
        ucontrol mine oX oY 0 0 0

        approach_ore:
        ucontrol approach oX oY 2 0 0
'''
a = "# Keep to mind that this has variation for different unit for faster logic\n"+a+"# End"
open('Temp\output.mlog', 'w').write(a)
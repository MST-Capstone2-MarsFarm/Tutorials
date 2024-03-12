#make sure you are in the same directory as this file when running it
my_function()
{
    echo "test"
}

export -f my_function

srun bash -c 'my_function'
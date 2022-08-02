<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('commute', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->Time('commuteStartTime');
            $table->Time('commuteFinishTime');
            $table->boolean('commuteIsActivity');
            $table->boolean('isCommute');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('commute');
    }
};

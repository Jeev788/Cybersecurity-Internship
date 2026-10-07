import mongoose from "mongoose";
const s=new mongoose.Schema({userId:{type:mongoose.Schema.Types.ObjectId,ref:"User",required:true},action:{type:String,required:true},resource:String,decisionId:{type:mongoose.Schema.Types.ObjectId,ref:"Decision"}},{timestamps:true});s.index({userId:1,createdAt:-1});export default mongoose.model("Activity",s);
